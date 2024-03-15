"""Fansly Download Functionality"""


import random

from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Column
from time import sleep

from .downloadstate import DownloadState
from .m3u8 import download_m3u8
from .types import DownloadType

from config import FanslyConfig
from errors import ApiError, DownloadError, DuplicateCountError, M3U8Error, MediaError
from fileio.dedupe import dedupe_media_file
from media import MediaItem
from pathio import set_create_directory_for_download
from textio import print_info, print_warning
from utils.common import batch_list


def download_media_infos(
            config: FanslyConfig,
            media_ids: list[str]
        ) -> list[dict]:

    media_infos: list[dict] = []

    for ids in batch_list(media_ids, config.BATCH_SIZE):
        media_ids_str = ','.join(ids)

        url = f'https://apiv3.fansly.com/api/v1/account/media?ids={media_ids_str}&ngsw-bypass=true'

        config.cors_options_request(url)

        media_info_response = config.http_session.get(
            url,
            headers=config.http_headers()
        )

        media_info_response.raise_for_status()

        if media_info_response.status_code == 200:
            media_info = media_info_response.json()

            if not media_info['success']:
                raise ApiError(
                    f"Could not retrieve media info for {media_ids_str} due to an "
                    f"API error - unsuccessful "
                    f"| content: \n{media_info}"
                )

            for info in media_info['response']:
                media_infos.append(info)

        else:
            raise DownloadError(
                f"Could not retrieve media info for {media_ids_str} due to an "
                f"error --> status_code: {media_info_response.status_code} "
                f"| content: \n{media_info_response.content.decode('utf-8')}"
            )

        # Slow down a bit to be sure
        sleep(random.uniform(0.4, 0.75))

    return media_infos


def download_media(config: FanslyConfig, state: DownloadState, accessible_media: list[MediaItem]):
    """Downloads all media items to their respective target folders."""
    if state.download_type == DownloadType.NOTSET:
        raise RuntimeError('Internal error during media download - download type not set on state.')

    # loop through the accessible_media and download the media files
    for media_item in accessible_media:
        # Verify that the duplicate count has not drastically spiked and
        # and if it did verify that the spiked amount is significantly
        # high to cancel scraping
        if config.use_duplicate_threshold \
                and state.duplicate_count > config.DUPLICATE_THRESHOLD \
                and config.DUPLICATE_THRESHOLD >= 50:
            raise DuplicateCountError(state.duplicate_count)

        # general filename construction & if content is a preview; add that into its filename
        filename = media_item.get_file_name()

        # "None" safeguards
        if media_item.mimetype is None:
            raise MediaError('MIME type for media item not defined. Aborting.')

        if media_item.download_url is None:
            raise MediaError('Download URL for media item not defined. Aborting.')

        # deduplication - part 1: decide if this media is even worth further processing; by media id
        if any([media_item.media_id in state.recent_photo_media_ids, media_item.media_id in state.recent_video_media_ids]):
            if config.show_downloads and config.show_skipped_downloads:
                print_info(f"Deduplication [Media ID]: {media_item.mimetype.split('/')[-2]} '{filename}' → skipped")
            state.duplicate_count += 1
            continue

        else:
            if 'image' in media_item.mimetype:
                state.recent_photo_media_ids.add(media_item.media_id)

            elif 'video' in media_item.mimetype:
                state.recent_video_media_ids.add(media_item.media_id)

            elif 'audio' in media_item.mimetype:
                state.recent_audio_media_ids.add(media_item.media_id)

        base_directory = set_create_directory_for_download(config, state)

        # for collections downloads we just put everything into the same folder
        if state.download_type == DownloadType.COLLECTIONS:
            file_save_path = base_directory / filename
            # compatibility for final "Download finished...!" print
            file_save_dir = file_save_path

        # for every other type of download; we do want to determine the sub-directory to save the media file based on the mimetype
        else:
            if 'image' in media_item.mimetype:
                file_save_dir = base_directory / "Pictures"

            elif 'video' in media_item.mimetype:
                file_save_dir = base_directory / "Videos"

            elif 'audio' in media_item.mimetype:
                file_save_dir = base_directory / "Audio"

            else:
                # if the mimetype is neither image nor video, skip the download
                print_warning(f"Unknown mimetype; skipping download for mimetype: '{media_item.mimetype}' | media_id: {media_item.media_id}")
                continue
            
            # decides to separate previews or not
            if media_item.is_preview and config.separate_previews:
                file_save_path = file_save_dir / 'Previews' / filename
                file_save_dir = file_save_dir / 'Previews'

            else:
                file_save_path = file_save_dir / filename

            if not file_save_dir.exists():
                file_save_dir.mkdir(parents=True)
        
        # if show_downloads is True / downloads should be shown
        if config.show_downloads:
            print_info(f"Downloading {media_item.mimetype.split('/')[-2]} '{filename}'")

        try:

            if media_item.file_extension == 'm3u8':
                # handle the download of a m3u8 file
                file_save_path = download_m3u8(
                    config,
                    m3u8_url=media_item.download_url,
                    save_path=file_save_path
                )

            else:
                # handle the download of a normal media file
                with config.http_session.get(
                            media_item.download_url,
                            stream=True,
                            headers=config.http_headers()
                        ) as response:

                    if response.status_code == 200:
                        text_column = TextColumn(f"", table_column=Column(ratio=1))
                        bar_column = BarColumn(bar_width=60, table_column=Column(ratio=5))

                        file_size = int(response.headers.get('content-length', 0))

                        # if file size is above 20 MB display loading bar
                        disable_loading_bar = False if file_size >= 20_000_000 else True

                        progress = Progress(
                            text_column,
                            bar_column,
                            expand=True,
                            transient=True,
                            disable=disable_loading_bar
                        )

                        task_id = progress.add_task('', total=file_size)

                        progress.start()

                        CHUNK_SIZE = 1_048_576

                        with open(file_save_path, 'wb') as output_file:
                            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                                if chunk:
                                    output_file.write(chunk)
                                    progress.advance(task_id, len(chunk))

                        progress.refresh()
                        progress.stop()

                    else:
                        raise DownloadError(
                            f"Download failed on filename {filename} due to an "
                            f"error --> status_code: {response.status_code} "
                            f"| content: \n{response.content.decode('utf-8')} [13]"
                        )

            is_dupe = dedupe_media_file(config, state, media_item.mimetype, file_save_path)

            # Is it a duplicate?
            if is_dupe:
                continue

            # We only count them if the file was actually kept
            state.pic_count += 1 if 'image' in media_item.mimetype else 0
            state.vid_count += 1 if 'video' in media_item.mimetype else 0

        except M3U8Error as ex:
            print_warning(f'Skipping invalid item: {ex}')

        # Slow down a bit to be sure
        sleep(random.uniform(0.4, 0.75))
