"""Download Fansly Albums"""
from fileio.dedupe import dedupe_init
from .common import process_batch_download
from .downloadstate import DownloadState
from .types import DownloadType

from config import FanslyConfig
from textio import input_enter_continue, print_error, print_info, print_warning
from utils.common import is_valid_content_id, get_content_id_from_request


def download_album(config: FanslyConfig, state: DownloadState):
    """Downloads Fansly Album."""

    # This is important for directory creation later on.
    state.download_type = DownloadType.ALBUM

    print_info(f"You have launched in Album download mode.")

    if config.album_id is not None:
        print_info(f"Trying to download album {config.album_id} as specified on the command-line ...")
        album_id = config.album_id
    elif not config.interactive:
        raise RuntimeError(
            'Album downloading is not supported in non-interactive mode '
            'unless an album link or ID is specified via command-line.'
        )

    else:
        print_info(f"Please enter the link or ID of the album you would like to download."
                   f"\n{17 * ' '}After you click on an album, it will show in your browsers URL bar."
                   )
        print()

        while True:
            requested_album = input(f"\n{17 * ' '}► Album Link or ID: ")
            album_id = get_content_id_from_request(requested_album)

            if is_valid_content_id(album_id):
                break

            else:
                print_error(f"The input string '{requested_album}' can not be a valid album link or ID."
                            f"\n{22 * ' '}The last few numbers in the URL are the album ID"
                            f"\n{22 * ' '}Example: 'https://fansly.com/collection/<creator>/478316699355983877'"
                            f"\n{22 * ' '}In the example, '478316699355983877' is the album ID.",
                            17
                            )

    # send a first request to get all available "accountMediaId" ids, which are basically media ids of every graphic listed on /collections
    album_response = config.get_api() \
        .get_album(album_id)

    if album_response.status_code == 200:
        album = album_response.json()
        media_orders = album['response']['albumContent']
        media_ids = [media['mediaOfferId'] for media in media_orders]

        if media_orders:
            state.creator_id = media_orders[0]['accountId']

            raw_response = config.get_api().get_creator_account_info_by_id(state.creator_id)

            if raw_response.status_code == 200:
                account = raw_response.json()['response'][0]
                state.creator_name = account['username']
            else:
                print_error(
                    f"Creator {state.creator_id} not found. Response code: "
                    f"{raw_response.status_code}"
                    f"\n{raw_response.text}",
                    23
                )

            # Deferred deduplication init because directory may have changed
            # depending on album creator (!= configured creator)
            dedupe_init(config, state)

            process_batch_download(media_ids, config, state)

            if state.duplicate_count > 0 and config.show_downloads and not config.show_skipped_downloads:
                print_info(
                    f"Skipped {state.duplicate_count} already downloaded media item{'' if state.duplicate_count == 1 else 's'}."
                )

        else:
            print_warning(f"Could not find any accessible content in the album.")

    else:
        print_error(
            f"Failed to download album {album_id}. Response code: "
            f"{album_response.status_code}\n{album_response.text}",
            23
        )
        input_enter_continue(config.interactive)
