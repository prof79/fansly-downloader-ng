#!/usr/bin/env python3

"""Fansly Downloader NG"""

__version__ = '0.9.7'
__date__ = '2024-03-22T21:16:00+01'
__maintainer__ = 'prof79'
__copyright__ = f'Copyright (C) 2023-2024 by {__maintainer__}'
__authors__ = [
    'prof79',
    'Avnsx',
    'pawnstar81',
    'UpAndDown666',
    'icewinterberry12',
]
__credits__ = [
    'Avnsx',
    'KasumiDev',
    'FletcherD',
    'XelaRellum',
    'sunbart',
]

# TODO: Remove pyffmpeg's "Github Activeness" message
# TODO: Fix in future: audio needs to be properly transcoded from mp4 to mp3, instead of just saved as
# TODO: Rate-limiting fix works but is terribly slow - would be nice to know how to interface with Fansly API properly
# TODO: Check whether messages are rate-limited too or not


import base64
import traceback

# from memory_profiler import profile
from datetime import datetime

from config import FanslyConfig, load_config, validate_adjust_config
from config.args import parse_args, map_args_to_config
from config.modes import DownloadMode
from download.core import *
from errors import *
from fileio.dedupe import dedupe_init
from pathio import delete_temporary_pyinstaller_files
from textio import (
    input_enter_close,
    input_enter_continue,
    print_error,
    print_info,
    print_warning,
    set_window_title,
)
from updater import self_update
from utils.common import open_location
from utils.statistics import *
from utils.timer import Timer


# tell PIL to be tolerant of files that are truncated
# ImageFile.LOAD_TRUNCATED_IMAGES = True

# turn off for our purpose unnecessary PIL safety features
# Image.MAX_IMAGE_PIXELS = None


def print_logo() -> None:
    """Prints the Fansly Downloader NG logo."""
    print(
        # Base64 code to display logo in console
        base64.b64decode(
            'CiAg4paI4paI4paI4paI4paI4paI4paI4pWXIOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilojilZfilojilojilZcgIOKWiOKWiOKVlyAgIOKWiOKWiOKVlyAgICDilojilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilojilZcgICAgIOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4pWXIAogIOKWiOKWiOKVlOKVkOKVkOKVkOKVkOKVneKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKVlyAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWd4paI4paI4pWRICDilZrilojilojilZcg4paI4paI4pWU4pWdICAgIOKWiOKWiOKWiOKWiOKVlyAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWQ4pWdICAgIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKWiOKWiOKVlwogIOKWiOKWiOKWiOKWiOKWiOKVlyAg4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4pWU4paI4paI4pWXIOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKVkSAgIOKVmuKWiOKWiOKWiOKWiOKVlOKVnSAgICAg4paI4paI4pWU4paI4paI4pWXIOKWiOKWiOKVkeKWiOKWiOKVkSDilojilojilojilZcgICAg4paI4paI4paI4paI4paI4paI4paI4pWR4paI4paI4paI4paI4paI4paI4pWU4pWd4paI4paI4paI4paI4paI4paI4pWU4pWdCiAg4paI4paI4pWU4pWQ4pWQ4pWdICDilojilojilZTilZDilZDilojilojilZHilojilojilZHilZrilojilojilZfilojilojilZHilZrilZDilZDilZDilZDilojilojilZHilojilojilZEgICAg4pWa4paI4paI4pWU4pWdICAgICAg4paI4paI4pWR4pWa4paI4paI4pWX4paI4paI4pWR4paI4paI4pWRICDilojilojilZEgICAg4paI4paI4pWU4pWQ4pWQ4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4pWQ4pWdIOKWiOKWiOKVlOKVkOKVkOKVkOKVnSAKICDilojilojilZEgICAgIOKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4pWRIOKVmuKWiOKWiOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKVkSAgICAgICDilojilojilZEg4pWa4paI4paI4paI4paI4pWR4paI4paI4paI4paI4paI4paI4paI4pWRICAgIOKWiOKWiOKVkSAg4paI4paI4pWR4paI4paI4pWRICAgICDilojilojilZEgICAgIAogIOKVmuKVkOKVnSAgICAg4pWa4pWQ4pWdICDilZrilZDilZ3ilZrilZDilZ0gIOKVmuKVkOKVkOKVkOKVneKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVneKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVneKVmuKVkOKVnSAgICAgICDilZrilZDilZ0gIOKVmuKVkOKVkOKVkOKVneKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVnSAgICDilZrilZDilZ0gIOKVmuKVkOKVneKVmuKVkOKVnSAgICAg4pWa4pWQ4pWdICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgZGV2ZWxvcGVkIG9uIGdpdGh1Yi5jb20vcHJvZjc5L2ZhbnNseS1kb3dubG9hZGVyLW5nCg=='
        ).decode('utf-8')
    )
    print(f"{(100 - len(__version__) - 1) // 2 * ' '}v{__version__}\n")


# @profile(precision=2, stream=open('memory_use.log', 'w', encoding='utf-8'))
def main(config: FanslyConfig) -> int:
    """The main logic of the downloader program.
    
    :param config: The program configuration.
    :type config: FanslyConfig

    :return: The exit code of the program.
    :rtype: int
    """
    exit_code = EXIT_SUCCESS

    timer = Timer('Total')

    timer.start()

    # Update window title with specific downloader version
    set_window_title(f"Fansly Downloader NG v{config.program_version}")

    print_logo()

    delete_temporary_pyinstaller_files()
    load_config(config)

    args = parse_args()
    # Note that due to config._sync_settings(), command-line arguments
    # may overwrite config.ini settings later on during validation
    # when the config may be saved again.
    # Thus a separate config_args.ini will be used for the session.
    map_args_to_config(args, config)

    self_update(config)

    validate_adjust_config(config)

    if config.user_names is None \
            or config.download_mode == DownloadMode.NOTSET:
        raise RuntimeError('Internal error - user name and download mode should not be empty after validation.')

    global_download_state = GlobalState()

    print()
    if not config.minimize_output:
        print_info(f'Token: {config.token}')
        print_info(f'Check Key: {config.check_key}')
        print_info(
            f'Device ID: {config.get_api().device_id} '
            f'({datetime.fromtimestamp(config.get_api().device_id_timestamp / 1000)})'
        )
        print_info(f'Session ID: {config.get_api().session_id}')

        # M3U8 fixing interim
        print()
        print_info(
            "Due to important memory usage and video format bugfixes, "
            "existing media items "
            f"\n{' ' * 16} need to be re-hashed (`_hash_`/`_hash1_` to `_hash2_`)."
            f"\n{' ' * 16} Affected files will automatically be renamed in the background."
        )
        print()

    for creator_name in sorted(config.user_names):
        with Timer(creator_name):
            try:
                state = DownloadState(creator_name=creator_name)

                # Special treatment for deviating folder names later
                if not config.download_mode == DownloadMode.SINGLE:
                    dedupe_init(config, state)

                if not config.minimize_output:
                    print_download_info(config)

                get_creator_account_info(config, state)

                # Download mode:
                # Normal: Downloads Timeline + Messages one after another.
                # Timeline: Scrapes only the creator's timeline content.
                # Messages: Scrapes only the creator's messages content.
                # Single: Fetch a single post by the post's ID. Click on a post to see its ID in the url bar e.g. ../post/1283493240234
                # Collection: Download all content listed within the "Purchased Media Collection"

                print_info(f'Download mode is: {config.download_mode_str()}')
                print()

                if config.download_mode == DownloadMode.SINGLE:
                    download_single_post(config, state)

                elif config.download_mode == DownloadMode.COLLECTION:
                    download_collections(config, state)

                else:
                    if any([config.download_mode == DownloadMode.MESSAGES,
                            config.download_mode == DownloadMode.NORMAL]):
                        download_messages(config, state)

                    if any([config.download_mode == DownloadMode.TIMELINE,
                            config.download_mode == DownloadMode.NORMAL]):
                        download_timeline(config, state)

                update_global_statistics(global_download_state, download_state=state)
                print_statistics(config, state)

                # open download folder
                if state.base_path is not None:
                    open_location(state.base_path, config.open_folder_when_finished, config.interactive)

            # Still continue if one creator failed
            except ApiAccountInfoError as e:
                print_error(str(e))
                input_enter_continue(config.interactive)
                exit_code = SOME_USERS_FAILED

    timer.stop()

    print_timing_statistics()

    print_global_statistics(config, global_download_state)

    return exit_code


if __name__ == '__main__':
    config = FanslyConfig(program_version=__version__)
    exit_code = EXIT_SUCCESS

    try:
        exit_code = main(config)

    except KeyboardInterrupt:
        # TODO: Should there be any clean-up or in-program handling during Ctrl+C?
        print()
        print_warning('Program aborted.')
        exit_code = EXIT_ABORT

    except ApiError as e:
        print()
        print_error(str(e))
        exit_code = API_ERROR

    except ConfigError as e:
        print()
        print_error(str(e))
        exit_code = CONFIG_ERROR

    except DownloadError as e:
        print()
        print_error(str(e))
        exit_code = DOWNLOAD_ERROR

    except Exception as e:
        print()
        print_error(f'An unexpected error occurred: {e}\n{traceback.format_exc()}')
        exit_code = UNEXPECTED_ERROR

    input_enter_close(config.prompt_on_exit)
    exit(exit_code)
