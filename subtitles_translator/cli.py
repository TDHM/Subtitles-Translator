import argparse
import time

from subtitles_translator.available_languages import AvailableLanguages
from subtitles_translator.ffmpeg_utils import extract_srt, insert_srt
from subtitles_translator.subtitles import Subtitles
from subtitles_translator.translator import Translator

if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(
        description="Translate the subtitles of the source movie and save a new movie file with translated subtitles."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help=(
            "path to the input movie (if ends with .mp4) or srt files (if ends with .srt) containing subtitles to be"
            " translated"
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help=(
            "desired path to the output movie (if ends with .mp4 and input is a movie) or srt files (if ends with .srt)"
            " containing translated subtitles"
        ),
    )
    parser.add_argument(
        "-s", "--source", type=str, required=True, help="language of the input subtitles (source language)"
    )
    parser.add_argument("-t", "--target", type=str, required=True, help="target language")
    # this behavior is not implemented yet
    parser.add_argument(
        "--copy",
        action="store_true",
        help=(
            "output a copy of the movie (default) or add translated subtitles in place. no effects if input is a SRT"
            " file"
        ),
    )
    args = parser.parse_args()

    if args.input.endswith(".mp4"):
        source_srt = extract_srt(args.input).split("\n")
    elif args.input.endswith(".srt"):
        if args.output.endswith(".mp4"):
            raise ValueError("MP4 output file inconsistent with SRT file input.")
        with open(args.input, "r+") as srt_file:
            source_srt = srt_file.read().splitlines()
    else:
        raise ValueError("Input file format not supported.")

    source_language = AvailableLanguages(args.source)
    target_language = AvailableLanguages(args.target)

    translator = Translator(source_language=source_language, target_language=target_language)
    subtitles = Subtitles(source_srt)

    translator.translate_subtitles(subtitles)

    if args.output.endswith(".mp4"):
        subtitles.save_srt()
        insert_srt(args.input, args.output, "translated.srt")
    elif args.output.endswith(".srt"):
        subtitles.save_srt(args.output)
    else:
        raise ValueError("Input file format not supported.")

    end = time.time()
    print("Time elapsed: ", end - start)
