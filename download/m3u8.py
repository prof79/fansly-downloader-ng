"""M3U8 Media Download Handling"""


import av
import concurrent.futures
import io

from av.audio.stream import AudioStream
from av.video.stream import VideoStream
from memory_profiler import profile
from pyffmpeg import FFmpeg
from m3u8 import M3U8
from pathlib import Path
from rich.table import Column
from rich.progress import BarColumn, TextColumn, Progress
from typing import Optional, Any

from config.fanslyconfig import FanslyConfig
from errors import M3U8Error
from utils.web import get_file_name_from_url, get_qs_value, split_url
from textio import print_error


def get_m3u8_cookies(m3u8_url: str) -> dict[str, Any]:
    """Parses an M3U8 URL and returns CloudFront cookies.
    """
    # Parse URL query string for required cookie values
    policy = get_qs_value(m3u8_url, 'Policy')
    key_pair_id = get_qs_value(m3u8_url, 'Key-Pair-Id')
    signature = get_qs_value(m3u8_url, 'Signature')

    cookies = {
        'CloudFront-Key-Pair-Id': key_pair_id,
        'CloudFront-Policy': policy,
        'CloudFront-Signature': signature,
    }

    return cookies


def get_m3u8_progress(disable_loading_bar: bool) -> Progress:
    """Returns a Rich progress bar customized for M3U8 Downloads.
    """
    text_column = TextColumn('', table_column=Column(ratio=1))
    bar_column = BarColumn(bar_width=60, table_column=Column(ratio=5))

    return Progress(
        text_column,
        bar_column,
        expand=True,
        transient=True,
        disable=disable_loading_bar,
    )


@profile(precision=2, stream=open('memory_use.log', 'w', encoding='utf-8'))
def download_m3u8_old(config: FanslyConfig, m3u8_url: str, save_path: Path) -> bool:
    """Download M3U8 content as MP4.
    
    :param config: The downloader configuration.
    :type config: FanslyConfig

    :param m3u8_url: The URL string of the M3U8 to download.
    :type m3u8_url: str

    :param save_path: The suggested file to save the video to.
        This will be changed to MP4 (.mp4).
    :type save_path: Path

    :return: True if successful or False otherwise.
    :rtype: bool
    """
    CHUNK_SIZE = 65_536

    # Remove file extension (.m3u8) from save_path
    save_path = save_path.parent / save_path.stem

    cookies = get_m3u8_cookies(m3u8_url)

    m3u8_base_url, m3u8_file_url = split_url(m3u8_url)

    # download the m3u8 playlist
    playlist_response = config.http_session.get(
        m3u8_file_url,
        headers=config.http_headers(),
        cookies=cookies,
    )

    if playlist_response.status_code != 200:
        print_error(
            f'Failed downloading m3u8; at playlist_content request. '
            f'Response code: {playlist_response.status_code}\n'
            f'{playlist_response.text}',
            12
        )
        return False

    playlist_text = playlist_response.text

    # parse the m3u8 playlist content using the m3u8 library
    playlist: M3U8 = M3U8(playlist_text, base_uri=m3u8_base_url)

    # get a list of all the .ts files in the playlist
    ts_files = [segment.absolute_uri for segment in playlist.segments if segment.uri.endswith('.ts')]

    # define a nested function to download a single .ts file and return the content
    def download_ts(ts_url: str) -> bytes:
        ts_response = config.http_session.get(
            ts_url,
            headers=config.http_headers(),
            cookies=cookies,
            stream=True,
        )

        buffer = io.BytesIO()

        for chunk in ts_response.iter_content(chunk_size=CHUNK_SIZE):
            buffer.write(chunk)

        ts_content = buffer.getvalue()

        return ts_content

    # Display loading bar if there are many segments
    progress = get_m3u8_progress(
        disable_loading_bar=len(ts_files) < 15
    )

    with progress:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            segment_bytes_list = [
                file for file in progress.track(
                    executor.map(download_ts, ts_files),
                    total=len(ts_files)
                )
            ]
    
    all_ts_bytes = bytearray()

    for segment_bytes in segment_bytes_list:
        all_ts_bytes += segment_bytes
    
    input_container = av.open(io.BytesIO(all_ts_bytes), format='mpegts')

    first_video_stream: Optional[VideoStream] = None
    first_audio_stream: Optional[AudioStream] = None

    for stream in input_container.streams.video:
        first_video_stream = stream
        break

    for stream in input_container.streams.audio:
        first_audio_stream = stream
        break

    has_video = first_video_stream is not None
    has_audio = first_audio_stream is not None

    if not has_video and not has_audio:
        raise M3U8Error(f'Neither audio nor video in M3U8 file: {m3u8_file_url}')

    # define output container and streams
    output_container = av.open(f"{save_path}.mp4", 'w') # add .mp4 file extension

    video_stream: Optional[VideoStream] = None
    audio_stream: Optional[AudioStream] = None

    if has_video:
        video_stream = output_container.add_stream(template=first_video_stream)

    if has_audio:
        audio_stream = output_container.add_stream(template=first_audio_stream)

    start_pts = None

    for packet in input_container.demux():

        if packet.dts is None:
            continue

        if start_pts is None:
            start_pts = packet.pts

        packet.pts -= start_pts
        packet.dts -= start_pts

        if packet.stream == first_video_stream:
            packet.stream = video_stream

        elif packet.stream == first_audio_stream:
            packet.stream = audio_stream

        output_container.mux(packet)

    # close containers
    input_container.close()
    output_container.close()

    return True


@profile(precision=2, stream=open('memory_use.log', 'w', encoding='utf-8'))
def download_m3u8(
            config: FanslyConfig,
            m3u8_url: str,
            save_path: Path,
        ) -> bool:
    """Download M3U8 content as MP4.
    
    :param config: The downloader configuration.
    :type config: FanslyConfig

    :param m3u8_url: The URL string of the M3U8 to download.
    :type m3u8_url: str

    :param save_path: The suggested file to save the video to.
        This will be changed to MP4 (.mp4).
    :type save_path: Path

    :return: True if successful or False otherwise.
    :rtype: bool
    """
    CHUNK_SIZE = 65_536

    cookies = get_m3u8_cookies(m3u8_url)

    m3u8_base_url, m3u8_file_url = split_url(m3u8_url)

    video_path = save_path.parent
    full_path = video_path / f'{save_path.stem}.mp4'

    with config.http_session.get(
                m3u8_file_url,
                headers=config.http_headers(),
                cookies=cookies,
            ) as stream_response:

        if stream_response.status_code != 200:
            print_error(
                f'Failed downloading M3U8 at playlist_content request. '
                f'Response code: {stream_response.status_code}\n'
                f'{stream_response.text}',
                12
            )
            return False        

        segments_text = stream_response.text

        segments_playlist = M3U8(
            content=segments_text,
            base_uri=m3u8_base_url,
        )

        if segments_playlist.is_endlist != True \
            or segments_playlist.playlist_type != 'vod':
                raise M3U8Error(f'Invalid video stream info for {m3u8_file_url}')

        #region Nested function to download TS segments
        def download_ts(segment_uri: str, segment_full_path: Path) -> None:
            with config.http_session.get(
                        segment_uri,
                        headers=config.http_headers(),
                        cookies=cookies,
                        stream=True
                    ) as segment_response:
                with open(segment_full_path, 'wb') as ts_file:
                    for chunk in segment_response.iter_content(CHUNK_SIZE):
                        if chunk is not None:
                            ts_file.write(chunk)
        #endregion

        segments = segments_playlist.segments

        segment_files: list[Path] = []
        segment_uris: list[str] = []

        for segment in segments:
            segment_uri = segment.absolute_uri

            segment_file_name = get_file_name_from_url(segment_uri)
            
            segment_full_path = video_path / segment_file_name

            segment_files.append(segment_full_path)
            segment_uris.append(segment_uri)

        # Display loading bar if there are many segments
        progress = get_m3u8_progress(
            disable_loading_bar=len(segment_files) < 5
        )

        ffmpeg_list_file = video_path / '_ffmpeg_concat_.ffc'

        try:

            with progress:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    _ = list(
                        progress.track(
                            executor.map(download_ts, segment_uris, segment_files),
                            total=len(segment_files)
                        )
                    )

            # Check multi-threaded downloads
            for file in segment_files:
                if not file.exists():
                    raise M3U8Error(f'Stream segment failed to download: {file}')

            with open(ffmpeg_list_file, 'w', encoding='utf-8') as list_file:
                list_file.write('ffconcat version 1.0\n')
                list_file.writelines([f"file '{f.name}'\n" for f in segment_files])

            ffmpeg = FFmpeg(enable_log=config.debug)

            ffmpeg.options(
                f'-f concat -i "{ffmpeg_list_file}" -c copy "{full_path}"'
            )

        finally:
            #region Clean up

            ffmpeg_list_file.unlink(missing_ok=True)

            for file in segment_files:
                file.unlink(missing_ok=True)
            
            #endregion

    return True
