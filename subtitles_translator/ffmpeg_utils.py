import subprocess as sp


def extract_srt(video_path: str) -> str:
    """Use FFmpeg to extract subtitles in srt format. Only the first subtitles track is extracted.

    Args:
        video_path (str): path to the movie file

    Returns:
        str: full subtitles in srt format
    """

    # Use subprocess to call FFmpeg CLI
    out = sp.run(["ffmpeg", "-i", video_path, "-map", "s:0", "-f", "srt", "-"], capture_output=True, text=True)
    subtitles = out.stdout

    return subtitles


def insert_srt(video_path: str, output_path: str, srt_path: str) -> None:
    """Use FFmpeg to insert a new subtitles track.

    Args:
        video_path (str): path to the source movie file
        output_path (str): desired path to the output movie file with new subtitles
        srt_path (str): path to the srt subtitles file
    """

    sp.run(["ffmpeg", "-i", video_path, "-i", srt_path, "-c", "copy", "-c:s", "mov_text", output_path])
