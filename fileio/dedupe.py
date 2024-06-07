"""Item Deduplication"""


from pathlib import Path
from random import randint

from config import FanslyConfig
from download.downloadstate import DownloadState
from fileio.fnmanip import add_hash_to_filename, add_hash_to_folder_items, get_hash_for_image, get_hash_for_other_content
from pathio import set_create_directory_for_download
from textio import print_info, print_warning


def dedupe_init(config: FanslyConfig, state: DownloadState):
    """Deduplicates (hashes) all existing media files in the
    target directory structure.
    
    Downloads can then be filtered for pre-existing files.
    """
    # This will create the base user path download_directory/creator_name
    set_create_directory_for_download(config, state)

    if state.download_path and state.download_path.is_dir():
        print_info(f"Deduplication is automatically enabled for:\n{17*' '}{state.download_path}")
        
        add_hash_to_folder_items(config, state)

        if not config.minimize_output:
            print_info(
                f"Deduplication process is complete! Each new download will now be compared"
                f"\n{17*' '}against a total of {len(state.recent_photo_hashes)} photo & {len(state.recent_video_hashes)} "
                "video hashes and corresponding media IDs."
            )

            # print("Recent Photo Hashes:", state.recent_photo_hashes)
            # print("Recent Photo Media IDs:", state.recent_photo_media_ids)
            # print("Recent Video Hashes:", state.recent_video_hashes)
            # print("Recent Video Media IDs:", state.recent_video_media_ids)

            if randint(1, 100) <= 19:
                print_warning(
                    f"Reminder: If you remove id_NUMBERS or hash_STRING from filenames of previously downloaded files"
                    f"\n{20*' '}they will no longer be compatible with Fansly Downloader's deduplication algorithm!"
                )

            # because adding information as metadata; requires specific
            # configuration for each file type through PIL and that's too complex
            # due to file types. maybe in the future I might decide to just save
            # every image as .png and every video as .mp4 and add/read it as
            # metadata or if someone contributes a function actually perfectly
            # adding metadata to all common file types, that would be nice.
        else:
            print()


def dedupe_media_file(config: FanslyConfig, state: DownloadState, mimetype: str, filename: Path) -> bool:
    """Hashes media file data and checks on-the-fly
    whether it is a duplicate or not.

    The hash will be added to the respective set of hashes if it is not
    a duplicate.

    :param DownloadState state: The current download state, for statistics and
        to populate the respective set of hashes.
    :param str mimetype: The MIME type of the media item.
    :param str filename: The full path of the file to examine.
    
    :return: True if it is a duplicate or False otherwise.
    :rtype: bool
    """
    file_hash = None
    hashlist = None

    # Use specific hashing for images
    if 'image' in mimetype:
        # open the image
        file_hash = get_hash_for_image(filename)
        
        hashlist = state.recent_photo_hashes

    else:
        file_hash = get_hash_for_other_content(filename)

        if 'audio' in mimetype:
            hashlist = state.recent_audio_hashes

        elif 'video' in mimetype:
            hashlist = state.recent_video_hashes

        else:
            raise RuntimeError('Internal error during media deduplication - invalid MIME type passed.')

    # Deduplication - part 2.1: decide if this media is even worth further processing; by hashing
    if file_hash in hashlist:
        if config.show_downloads and config.show_skipped_downloads:
            print_info(f"Deduplication [Hashing]: {mimetype.split('/')[-2]} '{filename.name}' → skipped")
        filename.unlink()
        state.duplicate_count += 1
        return True

    else:
        hashlist.add(file_hash)

        new_filename = Path(add_hash_to_filename(filename, file_hash))

        if new_filename.exists():
            filename.unlink()
        else:
            filename.rename(new_filename)

        return False
