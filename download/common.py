"""Common Download Functions"""

import traceback

from typing import Any

from .downloadstate import DownloadState
from .media import download_media
from .types import DownloadType

from config import FanslyConfig
from errors import DuplicateCountError, ApiError
from media import MediaItem, parse_media_info
from pathio import set_create_directory_for_download
from textio import print_error, print_info, print_warning, input_enter_continue


def get_unique_media_ids(info_object: dict[str, Any]) -> list[str]:
    """Extracts a unique list of media IDs from `accountMedia` and
    `accountMediaBundles` of prominent Fansly API objects.

    :param info_object: A dictionary object obtained via JSON representing
        a timeline, post or messages object.
    
    :return: An unique list of media ID strings.
    :rtype: list[str]
    """
    # Notes for the "bundles desaster":
    #
    # https://apiv3.fansly.com/api/v1/post?ids=XXX&ngsw-bypass=true
    # response.post.attachments.contentId
    # https://apiv3.fansly.com/api/v1/timelinenew/XXX?before=YYY&after=0&wallId=&contentSearch=&ngsw-bypass=true
    # response posts[0].attachments.contentId
    # points to response.accountMediaBundles
    #
    # response.accountMediaBundles[0].accountMediaIds
    # has media IDs (array) -> no locations, use "account/media" API!!!
    # response.accountMediaBundles[0]
    # has properties like "previewId" and "createdAt"

    account_media = info_object.get('accountMedia', [])
    media_bundles = info_object.get('accountMediaBundles', [])

    def check(item) -> bool:
        if item is None:
            raise ApiError(
                'Media items in response are empty - this is most probably a Fansly API/countermeasure issue.'
            )
        return True

    account_media_ids = [
        media['id']
        for media in account_media if check(media)
    ]

    bundle_media_ids = []

    media_id_bundles = [
        bundle['accountMediaIds']
        for bundle in media_bundles if check(bundle)
    ]

    # Flatten the ID lists
    for id_list in media_id_bundles:
        bundle_media_ids.extend(id_list)

    all_media_ids = set()

    for id in account_media_ids:
        all_media_ids.add(id)

    for id in bundle_media_ids:
        all_media_ids.add(id)

    return list(all_media_ids)


def print_download_info(config: FanslyConfig) -> None:
    ## starting here: stuff that literally every download mode uses, which should be executed at the very first everytime
    if config.user_agent:
        print_info(f"Using user-agent: '{config.user_agent[:28]} [...] {config.user_agent[-35:]}'")

    print_info(f"Open download folder when finished, is set to: '{config.open_folder_when_finished}'")
    print_info(f"Downloading files marked as preview, is set to: '{config.download_media_previews}'")
    print()

    if config.download_media_previews:
        print_warning('Previews downloading is enabled; repetitive and/or emoji spammed media might be downloaded!')
        print()


def process_download_accessible_media(
        config: FanslyConfig,
        state: DownloadState,
        media_infos: list[dict],
        post_id: str | None = None,
) -> bool:
    """Filters all media found in posts, messages, ... and downloads them.

    :param FanslyConfig config: The downloader configuration.
    :param DownloadState state: The state and statistics of what is
        currently being downloaded.
    :param list[dict] media_infos: A list of media informations from posts,
        timelines, messages, collections and so on.
    :param str|None post_id: The post ID required for "Single" download mode.

    :return: "False" as a break indicator for "Timeline" downloads,
        "True" otherwise.
    :rtype: bool
    """
    media_items: list[MediaItem] = []

    # Timeline

    # loop through the list of dictionaries and find the highest quality media URL for each one
    for media_info in media_infos:
        try:
            # add details into a list
            media_items += [parse_media_info(state, media_info, post_id)]

        except Exception:
            print_error(f"Unexpected error parsing {state.download_type_str()} content;\n{traceback.format_exc()}", 42)
            input_enter_continue(config.interactive)

    # summarise all scrapable & wanted media
    accessible_media = [
        item for item in media_items
        if item.download_url \
           and (item.is_preview == config.download_media_previews \
                or not item.is_preview)
    ]

    # Special messages handling
    original_duplicate_threshold = config.DUPLICATE_THRESHOLD

    if state.download_type == DownloadType.MESSAGES:
        state.total_message_items += len(accessible_media)

        # Overwrite base dup threshold with 20% of total accessible content in messages.
        # Don't forget to save/reset afterwards.
        config.DUPLICATE_THRESHOLD = int(0.2 * state.total_message_items)

    if not config.minimize_output:
        # at this point we have already parsed the whole post object and determined what is scrapable with the code above
        print_info(
            f"@{state.creator_name} - amount of media in {state.download_type_str()}: {len(media_infos)} (scrapable: {len(accessible_media)})")

    set_create_directory_for_download(config, state)

    try:
        # download it
        download_media(config, state, accessible_media)

    except DuplicateCountError:
        print_warning(
            f"Already downloaded all possible {state.download_type_str()} content! [Duplicate threshold exceeded {config.DUPLICATE_THRESHOLD}]")
        # "Timeline" needs a way to break the loop.
        if state.download_type == DownloadType.TIMELINE:
            return False

    except Exception:
        print_error(f"Unexpected error during {state.download_type_str()} download: \n{traceback.format_exc()}", 43)
        input_enter_continue(config.interactive)

    finally:
        # Reset DUPLICATE_THRESHOLD to the value it was before.
        config.DUPLICATE_THRESHOLD = original_duplicate_threshold

    return True
