"""Timeline Downloads"""


import random
import traceback

from requests import Response
from time import sleep

from .common import process_download_accessible_media
from .core import DownloadState
from .types import DownloadType

from config import FanslyConfig
from errors import ApiError
from textio import input_enter_continue, print_debug, print_error, print_info, print_warning


def download_timeline(config: FanslyConfig, state: DownloadState) -> None:

    print_info(f"Executing Timeline functionality. Anticipate remarkable outcomes!")
    print()

    # This is important for directory creation later on.
    state.download_type = DownloadType.TIMELINE

    # this has to be up here so it doesn't get looped
    timeline_cursor = 0
    attempts = 0

    # Careful - "retry" means (1 + retries) runs
    while True and attempts <= config.timeline_retries:
        if timeline_cursor == 0:
            print_info(f"Inspecting most recent Timeline cursor ... [CID: {state.creator_id}]")

        else:
            print_info(f"Inspecting Timeline cursor: {timeline_cursor} [CID: {state.creator_id}]")
    
        timeline_response = Response()
    
        try:
            timeline_url = \
                f"https://apiv3.fansly.com/api/v1/timelinenew/{state.creator_id}?before={timeline_cursor}&after=0&wallId=&contentSearch=&ngsw-bypass=true"

            config.cors_options_request(timeline_url)

            timeline_response = config.http_session.get(
                timeline_url,
                headers=config.http_headers(),
            )

            timeline_response.raise_for_status()

            if timeline_response.status_code == 200:

                post_object = timeline_response.json()['response']
        
                if config.debug:
                    print_debug(f'Post object: {post_object}')

                if len(post_object['accountMedia']) == 0:
                    # We might be a rate-limit victim, slow extremely down -
                    # but only if there are retries left
                    if attempts < config.timeline_retries:
                        print_info(f"Slowing down for {config.timeline_delay_seconds} s ...")
                        sleep(config.timeline_delay_seconds)
                    # Try again
                    attempts += 1
                    continue
                else:
                    # Reset attempts eg. new timeline
                    attempts = 0

                if not process_download_accessible_media(config, state, post_object['accountMedia']):
                    # Break on deduplication error - already downloaded
                    break

                print()

                # get next timeline_cursor
                try:
                    # Slow down to avoid the Fansly rate-limit which was introduced in late August 2023
                    sleep(random.uniform(2, 4))

                    timeline_cursor = post_object['posts'][-1]['id']

                except IndexError:
                    # break the whole while loop, if end is reached
                    break

                except Exception:
                    message = \
                        'Please copy & paste this on GitHub > Issues & provide a short explanation (34):'\
                        f'\n{traceback.format_exc()}\n'

                    raise ApiError(message)

        except KeyError:
            print_error("Couldn't find any scrapable media at all!\
                \n This most likely happend because you're not following the creator, your authorisation token is wrong\
                \n or the creator is not providing unlocked content.",
                35
            )
            input_enter_continue(config.interactive)

        except Exception:
            print_error(f"Unexpected error during Timeline download: \n{traceback.format_exc()}", 36)
            input_enter_continue(config.interactive)
