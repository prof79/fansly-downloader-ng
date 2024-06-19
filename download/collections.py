"""Download Fansly Collections"""

from .common import process_batch_download
from .downloadstate import DownloadState
from .types import DownloadType

from config import FanslyConfig
from textio import input_enter_continue, print_error, print_info


def download_collections(config: FanslyConfig, state: DownloadState):
    """Downloads Fansly purchased item collections."""

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

        process_batch_download(account_media_ids, config, state)

        if state.duplicate_count > 0 and config.show_downloads and not config.show_skipped_downloads:
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
