import argparse
import time

from ffmpeg_utils import extract_srt, insert_srt
from subtitles import Subtitles
from translator import Translator

if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(
        description="Translate the subtitles of the source movie and save a new movie file with translated subtitles."
    )
    parser.add_argument("-i", "--input", type=str, help="path to the input movie containing subtitles to be translated")
    parser.add_argument("-o", "--output", type=str, help="desired path to the output movie with translated subtitles")
    parser.add_argument(
        "-s", "--source", type=str, default="en", help="language of the input subtitles (source language)"
    )
    parser.add_argument("-t", "--target", type=str, default="fr", help="target language")
    parser.add_argument(
        "--copy", action="store_true", help="output a copy of the movie (default) or add translated subtitles in place"
    )
    args = parser.parse_args()

    source_srt = extract_srt(args.input).split("\n")

    translator = Translator(source_language=args.source, target_language=args.target)
    subtitles = Subtitles(source_srt)

    translator.translate_subtitles(subtitles)
    subtitles.save_srt()

    insert_srt(args.input, args.output, "translated.srt")

    end = time.time()
    print("Time elapsed: ", end - start)
