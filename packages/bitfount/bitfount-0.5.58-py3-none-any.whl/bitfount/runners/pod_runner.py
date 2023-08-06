"""Contains courtesy classes and functions for making pod running easier."""
import importlib
import logging
import os
from os import PathLike
from pathlib import Path
from typing import Union

import desert
from envyaml import EnvYAML

from bitfount.data.datasources.utils import OphthalmologyDataSourceArgs
from bitfount.data.datasplitters import DatasetSplitter
from bitfount.federated.keys_setup import _get_pod_keys
from bitfount.federated.pod import BaseSource, Pod
from bitfount.hub.helper import _create_access_manager, _create_bitfounthub
from bitfount.runners.config_schemas import PodConfig, PodDataConfig

logger = logging.getLogger(__name__)


def setup_pod_from_config_file(path_to_config_yaml: Union[str, PathLike]) -> Pod:
    """Creates a pod from a YAML config file.

    Args:
        path_to_config_yaml: The path to the config file.

    Returns:
        The created pod.
    """
    path_to_config_yaml = Path(path_to_config_yaml)
    logger.debug(f"Loading pod config from: {path_to_config_yaml}")

    # This double-underscore staticmethod access is not desirable but the additional
    # functionality in the class __init__ produces undesirable other inclusions.
    # This method allows us to just utilise the parsing aspect whilst performing
    # the envvar replacement.
    # TODO: [BIT-2202] Revisit double-underscore method usage.
    config_yaml = EnvYAML._EnvYAML__read_yaml_file(  # type: ignore[attr-defined] # Reason: see comment # noqa: B950
        path_to_config_yaml, os.environ, strict=True
    )

    pod_config_schema = desert.schema(PodConfig)
    pod_config_schema.context["config_path"] = path_to_config_yaml

    config = pod_config_schema.load(config_yaml)
    return setup_pod_from_config(config)


def setup_pod_from_config(config: PodConfig) -> Pod:
    """Creates a pod from a loaded config.

    Args:
        config: The configuration as a PodConfig instance.

    Returns:
        The created pod.
    """
    bitfount_hub = _create_bitfounthub(config.username, config.hub.url, config.secrets)
    access_manager = _create_access_manager(
        bitfount_hub.session, config.access_manager.url
    )

    # Load Pod Keys
    pod_directory = bitfount_hub.user_storage_path / "pods" / config.name
    pod_keys = _get_pod_keys(pod_directory)

    if config.datasource is not None and config.data_config is not None:
        datasource = setup_datasource(config.datasource, config.data_config)
    elif config.datasources is not None:
        datasource = setup_datasource(
            config.datasources[0].datasource, config.datasources[0].data_config
        )  # TODO: [BIT-2696] Only considering first dataset for now.
    else:
        raise ValueError("No valid datasource config found")

    return Pod(
        name=config.name,
        datasource=datasource,
        schema=config.schema,
        data_config=config.data_config,
        pod_details_config=config.pod_details_config,
        hub=bitfount_hub,
        message_service=config.message_service,
        access_manager=access_manager,
        pod_keys=pod_keys,
        approved_pods=config.approved_pods,
        differential_privacy=config.differential_privacy,
        update_schema=config.update_schema,
    )


def setup_datasource(datasource: str, data_config: PodDataConfig) -> BaseSource:
    """Creates a BaseSource from a DatasourceConfig.

    Args:
        config: The configuration as a DatasourceConfig instance.

    Returns:
        The created BaseSource.
    """
    try:
        datasource_cls = getattr(importlib.import_module("bitfount.data"), datasource)
    except AttributeError:
        raise ImportError(f"Unable to import {datasource} from bitfount.")

    data_split_config = data_config.data_split
    data_splitter = DatasetSplitter.create(
        data_split_config.data_splitter, **data_split_config.args
    )
    if "ophthalmology_args" in data_config.datasource_args:
        data_config.datasource_args["ophthalmology_args"] = OphthalmologyDataSourceArgs(
            **data_config.datasource_args["ophthalmology_args"]
        )

    datasource = datasource_cls(
        data_splitter=data_splitter, **data_config.datasource_args
    )

    if isinstance(datasource, BaseSource):
        return datasource
    else:
        raise ValueError(
            f"The configured datasource {datasource} does not extend BaseSource"
        )
