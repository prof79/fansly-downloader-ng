"""Statistics Calculation and Output"""


from time import sleep

from config import FanslyConfig
from download.core import DownloadState, GlobalState
from utils.timer import Timer
from textio import print_info


__all__ = [
    'update_global_statistics',
    'print_timing_statistics',
    'print_statistics',
    'print_global_statistics',
]


def update_global_statistics(global_state: GlobalState, download_state: DownloadState) -> None:
    """Updates the global statistics from each creator downloaded."""
    global_state.duplicate_count += download_state.duplicate_count
    global_state.pic_count += download_state.pic_count
    global_state.vid_count += download_state.vid_count
    global_state.total_message_items += download_state.total_message_items
    global_state.total_timeline_pictures += download_state.total_timeline_pictures
    global_state.total_timeline_videos += download_state.total_timeline_videos


def print_timing_statistics() -> None:
    message = ''

    def sec_to_text(timing: float) -> str:
        if timing >= 3600:
            return f'{(timing / 3600):0.2f} hours'

        elif timing >= 60:
            return f'{(timing / 60):0.2f} minutes'

        else:
            return f'{timing:0.2f} seconds'

    for timing in Timer.timers:
        if timing != 'Total':
            message += f"\n    @{timing}: {sec_to_text(Timer.timers[timing])}"
    
    message += f"\n\n Total execution time: {sec_to_text(Timer.timers['Total'])}"

    print_info(
        f"\n╔═\n  SESSION DURATION"
        f"\n"
        f"\n  Creators:"
        f"\n"
        f"{message}"
        f"\n{74*' '}═╝"        
    )


def print_statistics_helper(state: GlobalState, header: str, footer: str='') -> None:

    missing_message = ''

    if state.missing_items_count() > 0:
        missing_message = ' (this may indicate a problem)'

    print_info(
        f"{header}"
        f"\n  Total timeline media: {state.total_timeline_pictures} pictures & {state.total_timeline_videos} videos (= {state.total_timeline_items()} items)"
        f"\n  Total message media: {state.total_message_items}"
        f"\n  Total media (timeline & messages): {state.total_timeline_items() + state.total_message_items}"
        f"\n  Downloaded media: {state.pic_count} pictures & {state.vid_count} videos (= {state.total_downloaded_items()} items)"
        f"\n  Duplicates skipped: {state.duplicate_count}"
        f"\n  Missing items: {state.missing_items_count()}{missing_message}"
        f"{footer}"
        f"\n{74*' '}═╝"
    )


def print_statistics(config: FanslyConfig, state: DownloadState) -> None:

    header = \
        f"\n╔═\n  Finished {config.download_mode_str()} type download for @{state.creator_name}!"

    footer = ''

    if not state.following:
        footer += f"\n  Follow the creator to be able to scrape media!"
    
    elif not state.subscribed:
        footer += f"\n  Subscribe to the creator if you would like to get the entire content."
    
    elif not config.download_media_previews and state.missing_items_count() > 0:
        footer += f"\n  Try setting download_media_previews to True in the config.ini file."
        footer += f"\n  Doing so will help if the creator has marked all his content as previews."

    print_statistics_helper(state, header, footer)

    sleep(10)


def print_global_statistics(config: FanslyConfig, state: GlobalState) -> None:

    if config.user_names is None:
        raise RuntimeError('Internal error printing statistics - user names undefined.')

    header = \
        f"\n╔═\n  GRAND TOTAL DOWNLOAD SUMMARY" \
        f"\n  Finished downloading media for {len(config.user_names)} creators!"

    footer = ''

    if state.missing_items_count() > 0:
        footer += "\n  Make sure you are following and subscribed to all creators."

    print_statistics_helper(state, header, footer)
