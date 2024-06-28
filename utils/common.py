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


def is_valid_post_id(post_id: str) -> bool:
    """Validates a Fansly post ID.

    Valid post IDs must:
    
    - only contain digits
    - be longer or equal to 10 characters
    - not contain spaces
    
    :param post_id: The post ID string to validate.
    :type post_id: str

    :return: True or False.
    :rtype: bool
    """
    return all(
        [
            post_id.isdigit(),
            len(post_id) >= 10,
            not any(char.isspace() for char in post_id),
        ]
    )


def get_post_id_from_request(requested_post: str) -> str:
    """Strips post_id from a post link if necessary.
    Otherwise, the post_id is returned directly

    :param requested_post: The request made by the user.
    :type requested_post: str

    :return: The extracted post_id.
    :rtype: str
    """
    post_id = requested_post
    if requested_post.startswith("https://fansly.com/"):
        post_id = requested_post.split('/')[-1]
    return post_id


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
