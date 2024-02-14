"""FFmpeg Launcher Module"""


import subprocess

import shutil
ffmpeg_bin = shutil.which("ffmpeg")
if ffmpeg_bin is None:
    from pyffmpeg import FFmpeg
    ffmpeg = FFmpeg(enable_log=False)
    ffmpeg_bin = ffmpeg.get_ffmpeg_bin()


def run_ffmpeg(args: list[str]) -> bool:
    proc_args = [ffmpeg_bin]

    proc_args += args

    result = subprocess.run(
        proc_args,
        encoding='utf-8',
        capture_output=True,
        check=True,
    )

    return result.returncode == 0
