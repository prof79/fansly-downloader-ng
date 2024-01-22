"""FFmpeg Launcher Module"""


import subprocess

from pyffmpeg import FFmpeg


def run_ffmpeg(args: list[str]) -> bool:
    ffmpeg = FFmpeg(enable_log=False)

    ffmpeg_bin = ffmpeg.get_ffmpeg_bin()

    proc_args = [ffmpeg_bin]

    proc_args += args

    result = subprocess.run(
        proc_args,
        encoding='utf-8',
        capture_output=True,
        check=True,
    )

    return result.returncode == 0
