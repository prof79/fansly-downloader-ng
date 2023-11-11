"""Global Downloading State Management (Statistics)"""


from dataclasses import dataclass


@dataclass
class GlobalState(object):
    #region Fields

    # Counters
    duplicate_count: int = 0
    pic_count: int = 0
    vid_count: int = 0

    total_message_items: int = 0
    total_timeline_pictures: int = 0
    total_timeline_videos: int = 0

    #endregion

    #region Methods

    def total_timeline_items(self) -> int:
        """Gets the total count of media items in the timeline(s)."""
        return self.total_timeline_pictures + self.total_timeline_videos


    def total_downloaded_items(self) -> int:
        """Gets the total count of downloaded items from the
        timeline(s).
        """
        return self.pic_count + self.vid_count


    def missing_items_count(self) -> int:
        """Gets the count of media items neither downloaded nor
        present locally.
        """
        missing_items_count = self.total_timeline_items() \
            + self.total_message_items \
            - self.total_downloaded_items() \
            - self.duplicate_count

        # TODO: Single-post issue
        # Counter negative values when timeline item is zero but download isn't
        if missing_items_count < 0:
            missing_items_count = 0

        return missing_items_count

    #endregion
