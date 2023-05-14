import argparse
import time

from subtitles_translator.available_languages import AvailableLanguages
from subtitles_translator.ffmpeg_utils import extract_srt, insert_srt
from subtitles_translator.subtitles import Subtitles
from subtitles_translator.translator import Translator


def translate_subtitles_cli() -> None:
    """Command Line Interface for Neural Subtitles Translation.

    Parameters:
        -h (--help): Show CLI help message
        -i (--input): Path to the input movie (if ends with .mp4) or srt file (if ends with .srt) containing subtitles to be translated
        -o (--output): Path to the output movie (if ends with .mp4 and input is a movie) or srt file (if ends with .srt) containing translated subtitles
        -s (--source): Code for the language of source subtitles (the source MP4 must only contain one track of subtitles)
        -t (--target): Code for the target language after translation.

    Example:
        With the following command, subtitles from 'video.mp4' will be extracted and translated from 'french' to 'english'. The video containing translated subtitles will be saved as 'translated_video.mp4':

        ```shell
        subtitles_translator -i video.mp4 -o translated_video.mp4 -s fr -t en
        ```

    """

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


if __name__ == "__main__":
    start = time.time()

    translate_subtitles_cli()

    end = time.time()
    print("Time elapsed: ", end - start)
