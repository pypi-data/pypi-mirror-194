"""
The `mlflow_cortex` module provides an API for logging and loading Cortex models. This module
exports Cortex models with the following flavors:

:py:mod:`mlflow.pyfunc`
    Produced for use by generic pyfunc-based deployment tools and batch inference.
"""
# Standard Libraries
import logging
import os
import importlib

# External Libraries
import mlflow
from mlflow.models import Model, ModelSignature, ModelInputExample
from mlflow.models.model import MLMODEL_FILE_NAME
from mlflow.utils.environment import (
    _validate_env_arguments,
    _REQUIREMENTS_FILE_NAME,
)
from mlflow.utils.annotations import keyword_only
from mlflow.utils.model_utils import (
    _add_code_from_conf_to_system_path,
)
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import (
    RESOURCE_DOES_NOT_EXIST,
    DIRECTORY_NOT_EMPTY,
)
from mlflow.tracking.artifact_utils import _download_artifact_from_uri
from mlflow.utils.requirements_utils import (
    _check_requirement_satisfied,
    _parse_requirements,
)
from mlflow.utils import (
    PYTHON_VERSION,
    get_major_minor_py_version,
)
from mlflow.pyfunc import PyFuncModel

# Self import
import cortex_cli.core.mlflow.mlflow_cortex as mlflow_cortex


PY_VERSION = "python_version"


_logger = logging.getLogger(__name__)


FLAVOR_NAME = "cortex_python_function"
MAIN = "loader_module"
CODE = "code"
DATA = "data"
ENV = "env"
SERIALIZATION_FORMAT_PICKLE = "pickle"
SERIALIZATION_FORMAT_CLOUDPICKLE = "cloudpickle"
SUPPORTED_SERIALIZATION_FORMATS = [
    SERIALIZATION_FORMAT_PICKLE,
    SERIALIZATION_FORMAT_CLOUDPICKLE,
]

# File name to which custom objects cloudpickle is saved - used during save and load
_CUSTOM_OBJECTS_SAVE_PATH = "custom_objects.cloudpickle"


@keyword_only
def log_model(
    model,  # cortex_saved_model_dir,
    artifact_path,
    custom_objects=None,
    conda_env=None,
    # signature=None,
    input_example=None,
    registered_model_name=None,
    style=None,
):
    """

    :return:
    """
    return Model.log(
        model=model,  # cortex_saved_model_dir=vega_saved_model_dir,
        artifact_path=artifact_path,
        flavor=mlflow_cortex,
        conda_env=conda_env,
        registered_model_name=registered_model_name,
        # signature=signature,
        input_example=input_example,
        style=style,
    )


@keyword_only
def save_model(
    path,
    loader_module=None,
    data_path=None,
    code_path=None,
    conda_env=None,
    mlflow_model=None,
    python_model=None,
    artifacts=None,
    custom_objects=None,
    signature: ModelSignature = None,
    input_example: ModelInputExample = None,
    pip_requirements=None,
    extra_pip_requirements=None,
    metadata=None,
    **kwargs,
):
    """Save a cortex model to a local file or a run.


    """
    if os.path.exists(path):
        raise MlflowException(
            "Path '{}' already exists".format(path), DIRECTORY_NOT_EMPTY
        )
    os.makedirs(path)

    # save custom objects if there are custom objects
    if custom_objects is not None and custom_objects != {}:
        _save_keras_custom_objects(path, custom_objects)

    _validate_env_arguments(conda_env, pip_requirements, extra_pip_requirements)

    mlflow_model = kwargs.pop("model", mlflow_model)
    if len(kwargs) > 0:
        raise TypeError(f"save_model() got unexpected keyword arguments: {kwargs}")
    if code_path is not None:
        if not isinstance(code_path, list):
            raise TypeError("Argument code_path should be a list, not {}".format(type(code_path)))

    return mlflow.pyfunc.model._save_model_with_class_artifacts_params(
            path=path,
            python_model=python_model,
            artifacts=artifacts,
            conda_env=conda_env,
            code_paths=code_path,
            mlflow_model=mlflow_model,
            pip_requirements=pip_requirements,
            extra_pip_requirements=extra_pip_requirements,
        )


def _save_keras_custom_objects(path, custom_objects):
    """
    Save custom objects dictionary to a cloudpickle file so a model can be easily loaded later.

    :param path: An absolute path that points to the data directory within /path/to/model.
    :param custom_objects: Keras ``custom_objects`` is a dictionary mapping
                           names (strings) to custom classes or functions to be considered
                           during deserialization. MLflow saves these custom layers using
                           CloudPickle and restores them automatically when the model is
                           loaded with :py:func:`mlflow.keras.load_model` and
                           :py:func:`mlflow.pyfunc.load_model`.
    """
    import cloudpickle

    custom_objects_path = os.path.join(path, _CUSTOM_OBJECTS_SAVE_PATH)
    with open(custom_objects_path, "wb") as out_f:
        cloudpickle.dump(custom_objects, out_f)


def load_model(
    model_uri: str,
    suppress_warnings: bool = False,
    dst_path: str = None,
) -> PyFuncModel:
    """
    Load a model stored in Python function format.

    :param model_uri: The location, in URI format, of the MLflow model. For example:

                      - ``/Users/me/path/to/local/model``
                      - ``relative/path/to/local/model``
                      - ``s3://my_bucket/path/to/model``
                      - ``runs:/<mlflow_run_id>/run-relative/path/to/model``
                      - ``models:/<model_name>/<model_version>``
                      - ``models:/<model_name>/<stage>``
                      - ``mlflow-artifacts:/path/to/model``

                      For more information about supported URI schemes, see
                      `Referencing Artifacts <https://www.mlflow.org/docs/latest/concepts.html#
                      artifact-locations>`_.
    :param suppress_warnings: If ``True``, non-fatal warning messages associated with the model
                              loading process will be suppressed. If ``False``, these warning
                              messages will be emitted.
    :param dst_path: The local filesystem path to which to download the model artifact.
                     This directory must already exist. If unspecified, a local output
                     path will be created.
    """
    local_path = _download_artifact_from_uri(artifact_uri=model_uri, output_path=dst_path)

    if not suppress_warnings:
        _warn_dependency_requirement_mismatches(local_path)

    model_meta = Model.load(os.path.join(local_path, MLMODEL_FILE_NAME))

    conf = model_meta.flavors.get(FLAVOR_NAME)
    if conf is None:
        raise MlflowException(
            f'Model does not have the "{FLAVOR_NAME}" flavor',
            RESOURCE_DOES_NOT_EXIST,
        )
    model_py_version = conf.get(PY_VERSION)
    if not suppress_warnings:
        _warn_potentially_incompatible_py_version_if_necessary(model_py_version=model_py_version)

    _add_code_from_conf_to_system_path(local_path, conf, code_key=CODE)
    data_path = os.path.join(local_path, conf[DATA]) if (DATA in conf) else local_path
    model_impl = importlib.import_module(conf[MAIN])._load_pyfunc(data_path)
    predict_fn = conf.get("predict_fn", "predict")

    # Load custom Keras objects
    custom_objects = None
    custom_objects_path = None
    if os.path.isdir(model_uri):
        if os.path.isfile(os.path.join(model_uri, _CUSTOM_OBJECTS_SAVE_PATH)):
            custom_objects_path = os.path.join(model_uri, _CUSTOM_OBJECTS_SAVE_PATH)
    if custom_objects_path is not None:
        import cloudpickle

        with open(custom_objects_path, "rb") as in_f:
            pickled_custom_objects = cloudpickle.load(in_f)
            pickled_custom_objects.update(custom_objects)
            custom_objects = pickled_custom_objects
    
    if custom_objects is not None:
        get_custom_objects = importlib.import_module('tensorflow.keras.utils.get_custom_objects')
        for k, v in custom_objects.items():
            get_custom_objects()['k'] = v
    
    #Download nltk dependencies
    try:
        nltk = importlib.import_module('nltk')
        nltk.data.path.insert(0,'./nltk_data')
        nltk.download('all', download_dir='./nltk_data')
    except:
        pass

    return PyFuncModel(model_meta=model_meta, model_impl=model_impl, predict_fn=predict_fn)


def _warn_potentially_incompatible_py_version_if_necessary(model_py_version=None):
    """
    Compares the version of Python that was used to save a given model with the version
    of Python that is currently running. If a major or minor version difference is detected,
    logs an appropriate warning.
    """
    if model_py_version is None:
        _logger.warning(
            "The specified model does not have a specified Python version. It may be"
            " incompatible with the version of Python that is currently running: Python %s",
            PYTHON_VERSION,
        )
    elif get_major_minor_py_version(model_py_version) != get_major_minor_py_version(PYTHON_VERSION):
        _logger.warning(
            "The version of Python that the model was saved in, `Python %s`, differs"
            " from the version of Python that is currently running, `Python %s`,"
            " and may be incompatible",
            model_py_version,
            PYTHON_VERSION,
        )


def _warn_dependency_requirement_mismatches(model_path):
    """
    Inspects the model's dependencies and prints a warning if the current Python environment
    doesn't satisfy them.
    """
    req_file_path = os.path.join(model_path, _REQUIREMENTS_FILE_NAME)
    if not os.path.exists(req_file_path):
        return

    try:
        mismatch_infos = []
        for req in _parse_requirements(req_file_path, is_constraint=False):
            req_line = req.req_str
            mismatch_info = _check_requirement_satisfied(req_line)
            if mismatch_info is not None:
                mismatch_infos.append(str(mismatch_info))

        if len(mismatch_infos) > 0:
            mismatch_str = " - " + "\n - ".join(mismatch_infos)
            warning_msg = (
                "Detected one or more mismatches between the model's dependencies and the current "
                f"Python environment:\n{mismatch_str}\n"
                "To fix the mismatches, call `mlflow.pyfunc.get_model_dependencies(model_uri)` "
                "to fetch the model's environment and install dependencies using the resulting "
                "environment file."
            )
            _logger.warning(warning_msg)

    except Exception as e:
        _logger.warning(
            f"Encountered an unexpected error ({repr(e)}) while detecting model dependency "
            "mismatches. Set logging level to DEBUG to see the full traceback."
        )
        _logger.debug("", exc_info=True)
