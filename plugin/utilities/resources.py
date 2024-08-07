import os
from functools import lru_cache
from pathlib import Path

from plugin.exceptions import (
    ConfigurationException,
    UnkownException,
)

ENV_VARIABLE_PROFILE = "PROFILE"


@lru_cache
def get_plugin_directory_path() -> Path:
    """Find plugin directory path

    Raises:
        UnkownException: _description_

    Returns:
        Path: path to plugin directory
    """
    plugin_dirs = [
        p for p in Path(__file__).parents if p.name == get_plugin_name()
    ]

    if not plugin_dirs:
        msg = "Couldn't find plugin folder"
        raise UnkownException(msg)

    return plugin_dirs[0]


@lru_cache
def read_metadata_file() -> str:
    """Get the contents of plugin metadata.txt file

    Raises:
        FileNotFoundError: raised if metadata.txt file could not be found

    Returns:
        str: metadata file content as a string
    """
    metadata_file = Path(__file__).absolute().parent.parent / "metadata.txt"

    if not metadata_file.exists():
        raise FileNotFoundError(metadata_file)

    return metadata_file.read_text("utf-8")


def get_plugin_name() -> str:
    """Get plugin name from metadata.txt file

    Raises:
        ValueError: raised if 'name=' row could not be found from
            metadata.txt file

    Returns:
        str: plugin name
    """
    metadata_str = read_metadata_file()

    for line in metadata_str.splitlines():
        if line.startswith("name="):
            name = line.split("=")[1].strip()
            break

    if not name:
        raise ValueError

    return name.replace(" ", "").strip()


def get_env_variable(
    variable_key: str, default_value: str | None = None
) -> str:
    """Get environment variable

    Args:
        variable_key (str): environment variable key
        default_value (_type_, optional): default value for environment
            variable if not found. Defaults to None.

    Returns:
        str: environment variable
    """
    return os.environ.get(variable_key, default_value)  # type: ignore


def get_resource_path(filename: str) -> Path:
    """Get path to the resource file.

    The path is path to the file from plugin's resource folder 'resources'.

    For example get_resource_path("icon.png")

    Args:
        filename (str): _description_

    Returns:
        Path: _description_
    """
    return get_plugin_directory_path() / "resources" / filename


def get_profile() -> str:
    """Get profile from environment variable

    Raises:
        QgisPluginConfigException:

    Returns:
        str: profile name
    """
    try:
        return os.environ[ENV_VARIABLE_PROFILE]
    except KeyError as e:
        err_msg = f"Ympäristömuuttujaa {ENV_VARIABLE_PROFILE} ei määritetty"
        raise ConfigurationException(err_msg) from e


@lru_cache
def resolve_api_version() -> str:
    """Reads and returns api version.

    Read the data from given root plugin path metadata.txt file.

    Returns:
        str: api version
    """
    api_version = "0.0"

    metadata_str = read_metadata_file()
    for line in metadata_str.splitlines():
        if line.startswith("apiVersion="):
            api_version = line.split("=")[1].strip()
            break

    return api_version
