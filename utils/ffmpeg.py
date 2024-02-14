"""FFmpeg Launcher Module"""


import shutil
import subprocess


def get_ffmpeg_bin() -> str:
    ffmpeg_bin = shutil.which("ffmpeg")

    if ffmpeg_bin is None:
        from pyffmpeg import FFmpeg
        ffmpeg = FFmpeg(enable_log=False)
        ffmpeg_bin = ffmpeg.get_ffmpeg_bin()

    return ffmpeg_bin


def run_ffmpeg(args: list[str]) -> bool:
    proc_args = [get_ffmpeg_bin()]

    proc_args += args

    result = subprocess.run(
        proc_args,
        encoding='utf-8',
        capture_output=True,
        check=True,
    )

    return result.returncode == 0
