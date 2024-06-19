"""Common Utility Functions"""

import os
import platform
import subprocess

from pathlib import Path
from typing import Any, Iterable

from config.fanslyconfig import FanslyConfig
from errors import ConfigError


def batch_list(input_list: list[Any], batch_size: int) -> Iterable[list[Any]]:
    """Yield successive n-sized batches from input_list.
    
    :param input_list: An arbitrary list to split into equal-sized chunks.
    :type input_list: list[Any]

    :param batch_size: The number of elements in a chunk to
        split the list into. Batch size must be >= 1.
    :type batch_size: int

    :return: An iterable of sub-lists of size `batch_size`.
    :rtype: Iterable[list[Any]]
    """
    if batch_size < 1:
        raise ValueError(f'batch_list(): Invalid batch size of {batch_size} is less than 1.')

    for i in range(0, len(input_list), batch_size):
        yield input_list[i:i + batch_size]


def save_config_or_raise(config: FanslyConfig) -> bool:
    """Tries to save the configuration to `config.ini` or
    raises a `ConfigError` otherwise.

    :param config: The program configuration.
    :type config: FanslyConfig

    :return: True if configuration was successfully written.
    :rtype: bool

    :raises ConfigError: When the configuration file could not be saved.
        This may be due to invalid path issues or permission/security
        software problems.
    """
    if not config._save_config():
        raise ConfigError(
            f"Internal error: Configuration data could not be saved to '{config.config_path}'. "
            "Invalid path or permission/security software problem."
        )
    else:
        return True


def is_valid_content_id(content_id: str) -> bool:
    """Validates a Fansly post / album ID.

    Valid post / album IDs must:
    
    - only contain digits
    - be longer or equal to 10 characters
    - not contain spaces
    
    :param content_id: The post / album ID string to validate.
    :type content_id: str

    :return: True or False.
    :rtype: bool
    """
    return all(
        [
            content_id.isdigit(),
            len(content_id) >= 10,
            not any(char.isspace() for char in content_id),
        ]
    )


def get_content_id_from_request(requested_content: str) -> str:
    """Strips post / album ID from a post / album link if necessary.
    Otherwise, the ID is returned directly

    :param requested_content: The request made by the user.
    :type requested_content: str

    :return: The extracted post / album ID.
    :rtype: str
    """
    content_id = requested_content
    if requested_content.startswith("https://fansly.com/"):
        content_id = requested_content.split('/')[-1]
    return content_id


def get_post_ids_from_list_of_requests(requested_posts: list[str]) -> list[str]:
    """Strips post_ids from a list of post links if necessary.

    :param requested_posts: The list of requests made by the user.
    :type requested_posts: list[str]

    :return: A list of extracted post_ids.
    :rtype: list[str]
    """
    post_ids = []
    for requested_post in requested_posts:
        post_ids.append(get_content_id_from_request(requested_post))
    return post_ids


def open_location(filepath: Path, open_folder_when_finished: bool, interactive: bool) -> bool:
    """Opens the download directory in the platform's respective
    file manager application once the download process has finished.

    :param filepath: The base path of all downloads.
    :type filepath: Path
    :param open_folder_when_finished: Open the folder or do nothing.
    :type open_folder_when_finished: bool
    :param interactive: Running interactively or not.
        Folder will not be opened when set to False.
    :type interactive: bool

    :return: True when the folder was opened or False otherwise.
    :rtype: bool
    """
    plat = platform.system()

    if not open_folder_when_finished or not interactive:
        return False

    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
        return False

    # tested below and they work to open folder locations
    if plat == 'Windows':
        # verified works
        os.startfile(filepath)

    elif plat == 'Linux':
        # verified works
        subprocess.run(['xdg-open', filepath], shell=False)

    elif plat == 'Darwin':
        # verified works
        subprocess.run(['open', filepath], shell=False)

    return True
