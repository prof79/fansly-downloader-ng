"""Fansly Account Information"""

import requests

from typing import Any

from .downloadstate import DownloadState

from config import FanslyConfig
from config.modes import DownloadMode
from errors import ApiAccountInfoError, ApiAuthenticationError, ApiError
from textio import print_info


def get_creator_account_info(config: FanslyConfig, state: DownloadState) -> None:
    if not config.minimize_output:
        print_info('Getting account information ...')

    if config.download_mode == DownloadMode.NOTSET:
        message = 'Internal error getting account info - config download mode not set.'
        raise RuntimeError(message)

    if state.creator_name is None:
        message = 'Internal error getting account info - creator name not set.'
        raise RuntimeError(message)

    # Collections are independent of creators and
    # single posts may diverge from configured creators
    if any([config.download_mode == DownloadMode.MESSAGES,
            config.download_mode == DownloadMode.NORMAL,
            config.download_mode == DownloadMode.TIMELINE]):

        account: dict[str, Any] = {}

        raw_response = requests.Response()

        try:
            raw_response = config.get_api() \
                .get_creator_account_info(state.creator_name)

            account = raw_response.json()['response'][0]

            state.creator_id = account['id']

        except KeyError as e:

            if raw_response.status_code == 401:
                message = \
                    f"API returned unauthorized (24). " \
                    f"This is most likely because of a wrong authorization " \
                    f"token in the configuration file." \
                    f"\n{21 * ' '}Have you surfed Fansly on this browser recently?" \
                    f"\n{21 * ' '}Used authorization token: '{config.token}'" \
                    f'\n  {str(e)}\n  {raw_response.text}'

                raise ApiAuthenticationError(message)

            else:
                message = \
                    'Bad response from fansly API (25). Please make sure your configuration file is not malformed.' \
                    f'\n  {str(e)}\n  {raw_response.text}'

                raise ApiError(message)

        except IndexError as e:
            message = \
                'Bad response from fansly API (26). Please make sure your configuration file is not malformed; most likely misspelled the creator name.' \
                f'\n  {str(e)}\n  {raw_response.text}'

            raise ApiAccountInfoError(message)

        # below only needed by timeline; but wouldn't work without acc_req so it's here
        # determine if followed
        state.following = account.get('following', False)

        # determine if subscribed
        state.subscribed = account.get('subscribed', False)

        # intentionally only put pictures into try / except block - its enough
        try:
            state.total_timeline_pictures = account['timelineStats']['imageCount']

        except KeyError:
            raise ApiAccountInfoError(
                f"Can not get timelineStats for creator username '{state.creator_name}'; you most likely misspelled it! (27)")

        state.total_timeline_videos = account['timelineStats']['videoCount']

        # overwrite base dup threshold with custom 20% of total timeline content
        config.DUPLICATE_THRESHOLD = int(0.2 * int(state.total_timeline_pictures + state.total_timeline_videos))

        # timeline & messages will always use the creator name from config.ini, so we'll leave this here
        print_info(f"Targeted creator: '{state.creator_name}'")
        print()
