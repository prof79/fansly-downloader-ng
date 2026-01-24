"""Message Downloading"""


import random

from time import sleep

from .common import get_unique_media_ids, process_download_accessible_media
from .downloadstate import DownloadState
from .media import download_media_infos
from .types import DownloadType

from config import FanslyConfig
from textio import input_enter_continue, print_error, print_info, print_warning


def download_messages(config: FanslyConfig, state: DownloadState):
    # This is important for directory creation later on.
    state.download_type = DownloadType.MESSAGES

    print_info(f"Initiating Messages procedure. Standby for results.")
    print()
    
    groups_response = config.get_api() \
        .get_group()

    if groups_response.status_code == 200:
        groups_response = groups_response.json()['response']['aggregationData']['groups']

        # go through messages and check if we even have a chat history with the creator
        group_id = None

        for group in groups_response:
            for user in group['users']:
                if user['userId'] == state.creator_id:
                    group_id = group['id']
                    break

            if group_id:
                break

        # only if we do have a message ("group") with the creator
        if group_id:

            msg_cursor: str = '0'

            while True:
                starting_duplicates = state.duplicate_count

                params = {'groupId': group_id, 'limit': '25', 'ngsw-bypass': 'true'}

                if msg_cursor != '0':
                    params['before'] = msg_cursor

                messages_response = config.get_api() \
                    .get_message(params)

                if messages_response.status_code == 200:
                
                    # Object contains: messages, accountMedia, accountMediaBundles, tips, tipGoals, stories
                    messages = messages_response.json()['response']

                    all_media_ids = get_unique_media_ids(messages)
                    media_infos = download_media_infos(config, all_media_ids)

                    process_download_accessible_media(config, state, media_infos)

                    # Print info on skipped downloads if `show_skipped_downloads` is enabled
                    skipped_downloads = state.duplicate_count - starting_duplicates
                    if skipped_downloads > 1 and config.show_downloads and not config.show_skipped_downloads:
                        print_info(
                            f"Skipped {skipped_downloads} already downloaded media item{'' if skipped_downloads == 1 else 's'}."
                        )

                    print()

                    # get next cursor
                    try:
                        # Fansly rate-limiting fix
                        # (don't know if messages were affected at all)
                        sleep(random.uniform(2, 4))
                        msg_cursor = messages['messages'][-1]['id']

                    except IndexError:
                        break # break if end is reached

                else:
                    print_error(
                        f"Failed messages download. messages_req failed with response code: "
                        f"{messages_response.status_code}\n{messages_response.text}", 
                        30
                    )

        elif group_id is None:
            print_warning(
                f"Could not find a chat history with "
                f"{state.creator_name}; skipping messages download ..."
            )

    else:
        print_error(
            f"Failed Messages download. Response code: "
            f"{groups_response.status_code}\n{groups_response.text}",
            31
        )
        input_enter_continue(config.interactive)
