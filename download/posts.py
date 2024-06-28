"""Posts Downloading"""


from .common import get_unique_media_ids, process_download_accessible_media
from .core import DownloadState
from .media import download_media_infos
from .types import DownloadType

from config import FanslyConfig
from fileio.dedupe import dedupe_init
from textio import input_enter_continue, print_error, print_info, print_warning
from utils.common import is_valid_post_id


def download_posts(config: FanslyConfig, state: DownloadState):
    """Downloads all desired posts."""

    # This is important for directory creation later on.
    state.download_type = DownloadType.POSTS

    print_info(f"You have launched in Posts download mode.")

    if config.post_ids is not None:
        print_info(f"Trying to download posts {config.post_ids} as specified on the command-line ...")
        post_ids = config.post_ids

    elif not config.interactive:
        raise RuntimeError(
            'Posts downloading is not supported in non-interactive mode '
            'unless post IDs are specified via command-line.'
        )

    else:
        print_info(f"Please enter the IDs of the posts you would like to download one after another (confirm with <Enter>)."
            f"\n{17*' '}After you click on a post, it will show in your browsers URL bar."
        )
        print()

        post_ids = []
        post_id = "dummy"

        while len(post_id) > 0:
            while True:
                post_id = input(f"\n{17*' '}► Post ID: ")

                if len(post_id) == 0:
                    print_info("All desired post IDs are recorded. Proceeding to download.")
                    break
                elif is_valid_post_id(post_id):
                    post_ids.append(post_id)
                    print_info(f"Post {post_id} is recorded. Enter the next one or hit enter to proceed.")
                    break
                else:
                    print_error(f"The input string '{post_id}' can not be a valid post ID."
                        f"\n{22*' '}The last few numbers in the url is the post ID"
                        f"\n{22*' '}Example: 'https://fansly.com/post/1283998432982'"
                        f"\n{22*' '}In the example, '1283998432982' would be the post ID.",
                        17
                    )

    for post_id in post_ids:

        post_response = config.get_api() \
            .get_post(post_id)

        if post_response.status_code == 200:
            # From: "accounts"
            creator_username, creator_display_name = None, None

            # post object contains: posts, aggregatedPosts, accountMediaBundles, accountMedia, accounts, tips, tipGoals, stories, polls
            post_object = post_response.json()['response']

            # if access to post content / post contains content
            if post_object['accountMediaBundles'] or post_object['accountMedia']:

                # parse post creator name
                if creator_username is None:
                    # the post creators reliable accountId
                    if post_object['accountMediaBundles']:
                        state.creator_id = post_object['accountMediaBundles'][0]['accountId']
                    else:
                        state.creator_id = post_object['accountMedia'][0]['accountId']

                    creator_display_name, creator_username = next(
                        (account.get('displayName'), account.get('username'))
                        for account in post_object.get('accounts', [])
                        if account.get('id') == state.creator_id
                    )

                    # Override the creator's name with the one from the posting.
                    # Post ID could be from a different creator than specified
                    # in the config file.
                    state.creator_name = creator_username

                    if creator_display_name and creator_username:
                        print_info(f"Inspecting a post by {creator_display_name} (@{creator_username})")
                    else:
                        print_info(f"Inspecting a post by {creator_username.capitalize()}")

                # Deferred deduplication init because directory may have changed
                # depending on post creator (!= configured creator)
                dedupe_init(config, state)

                all_media_ids = get_unique_media_ids(post_object)
                media_infos = download_media_infos(config, all_media_ids)

                process_download_accessible_media(config, state, media_infos, post_id)

                if state.duplicate_count > 0 and config.show_downloads and not config.show_skipped_downloads:
                    print_info(
                        f"Skipped {state.duplicate_count} already downloaded media item{'' if state.duplicate_count == 1 else 's'}."
                    )

            else:
                print_warning(f"Could not find any accessible content in post {post_id}.")

        else:
            print_error(f"Failed to download post {post_id}. Response code: {post_response.status_code}\n{post_response.text}", 20)
            input_enter_continue(config.interactive)
