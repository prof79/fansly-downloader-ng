"""Download Fansly Collections"""


from .common import process_download_accessible_media
from .downloadstate import DownloadState
from .types import DownloadType

from config import FanslyConfig
from textio import input_enter_continue, print_error, print_info
from utils.common import batch_list


def download_collections(config: FanslyConfig, state: DownloadState):
    """Downloads Fansly purchased item collections."""

    print_info(f"Starting Collections sequence. Buckle up and enjoy the ride!")

    # This is important for directory creation later on.
    state.download_type = DownloadType.COLLECTIONS

    # send a first request to get all available "accountMediaId" ids, which are basically media ids of every graphic listed on /collections
    collections_response = config.http_session.get(
        'https://apiv3.fansly.com/api/v1/account/media/orders/',
        params={'limit': '9999','offset': '0','ngsw-bypass': 'true'},
        headers=config.http_headers()
    )

    if collections_response.status_code == 200:
        collections = collections_response.json()
        account_media_orders = collections['response']['accountMediaOrders']
        account_media_ids = [order['accountMediaId'] for order in account_media_orders]
  
        # Splitting the list into batches and making separate API calls for each
        for batch in batch_list(account_media_ids, config.BATCH_SIZE):

            batched_ids = ','.join(batch)

            post_object_response = config.http_session.get(
                f"https://apiv3.fansly.com/api/v1/account/media?ids={batched_ids}",
                headers=config.http_headers())

            if post_object_response.status_code == 200:
                post_object = post_object_response.json()
    
                process_download_accessible_media(config, state, post_object['response'])
            
            else:
                print_error(
                    f"Media batch download failed. Response code: "
                    f"{post_object_response.status_code}"
                    f"\n{post_object_response.text}"
                    f"\n\nAffected media IDs: {batched_ids}",
                    23
                )
                input_enter_continue(config.interactive)


    else:
        print_error(
            f"Collections download failed. Response code: "
            f"{collections_response.status_code}\n{collections_response.text}",
            23
        )
        input_enter_continue(config.interactive)
