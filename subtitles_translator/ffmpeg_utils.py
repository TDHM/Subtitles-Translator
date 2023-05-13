"""Binding function to use FFmpeg.

This module provides Python binding functions to extract/insert subtitles to/from SRT files
using FFmpeg.

"""

import subprocess as sp


def extract_srt(video_path: str) -> str:
    """Use FFmpeg to extract subtitles in SRT format. Only the first subtitles track is extracted.

    Args:
        video_path (str): Path to the movie file

    Returns:
        str: Full subtitles in srt format

    """

    # Use subprocess to call FFmpeg CLI
    out = sp.run(["ffmpeg", "-i", video_path, "-map", "s:0", "-f", "srt", "-"], capture_output=True, text=True)
    subtitles = out.stdout

    return subtitles


def insert_srt(video_path: str, output_path: str, srt_path: str) -> None:
    """Use FFmpeg to insert a new subtitles track.

    Args:
        video_path (str): Path to the source movie file
        output_path (str): Desired path to the output movie file with new subtitles
        srt_path (str): Path to the SRT subtitles file

    """

    # ffmpeg convert SRT (SubRip) to MP4-compliant subtitles with -c:s mov_text
    sp.run(
        [
            "ffmpeg",
            "-i",
            video_path,
            "-f",
            "srt",
            "-i",
            srt_path,
            "-map",
            "0:0",
            "-map",
            "0:1",
            "-map",
            "1:0",
            "-c:v",
            "copy",
            "-c",
            "copy",
            "-c:s",
            "mov_text",
            output_path,
        ]
    )
