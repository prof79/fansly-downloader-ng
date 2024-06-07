"""Download Fansly Collections"""

from .common import process_download_accessible_media
from .downloadstate import DownloadState
from .types import DownloadType

from config import FanslyConfig
from textio import input_enter_continue, print_error, print_info
from utils.common import batch_list


def download_collections(config: FanslyConfig, state: DownloadState):
    """Downloads Fansly purchased item collections."""

    if not config.minimize_output:
        print_info(f"Starting Collections sequence. Buckle up and enjoy the ride!")

    # This is important for directory creation later on.
    state.download_type = DownloadType.COLLECTIONS

    # send a first request to get all available "accountMediaId" ids, which are basically media ids of every graphic listed on /collections
    collections_response = config.get_api() \
        .get_media_collections()

    if collections_response.status_code == 200:
        collections = collections_response.json()
        account_media_orders = collections['response']['accountMediaOrders']
        account_media_ids = [order['accountMediaId'] for order in account_media_orders]

        # Splitting the list into batches and making separate API calls for each
        for batch in batch_list(account_media_ids, config.BATCH_SIZE):

            batched_ids = ','.join(batch)

            media_info_response = config.get_api() \
                .get_account_media(batched_ids)

            if media_info_response.status_code == 200:
                media_info = media_info_response.json()['response']

                process_download_accessible_media(config, state, media_info)

            else:
                print_error(
                    f"Media batch download failed. Response code: "
                    f"{media_info_response.status_code}"
                    f"\n{media_info_response.text}"
                    f"\n\nAffected media IDs: {batched_ids}",
                    23
                )
                input_enter_continue(config.interactive)

        if state.duplicate_count > 0 and config.show_downloads and not config.show_skipped_downloads and not config.minimize_output:
            print_info(
                f"Skipped {state.duplicate_count} already downloaded media item{'' if state.duplicate_count == 1 else 's'}."
            )


    else:
        print_error(
            f"Collections download failed. Response code: "
            f"{collections_response.status_code}\n{collections_response.text}",
            23
        )
        input_enter_continue(config.interactive)
