"""Video Resolutions"""

from enum import IntEnum


class VideoResolution(IntEnum):
    NOTSET = 0
    RES_360 = 360
    RES_480 = 480
    RES_720 = 720
    RES_1080 = 1080
    RES_1440 = 1440
    RES_2160 = 2160

    @property
    def description(self):
        descriptions = {
            0: "Resolution not set",
            360: "Low Quality",
            480: "SD",
            720: "HD",
            1080: "Full HD",
            1440: "2K",
            2160: "4K"
        }
        return descriptions.get(self.value, "Unknown Resolution")
