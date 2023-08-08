from __future__ import annotations

import subprocess as sp


def test_translate_subtitles_cli():
    sp.run(
        [
            "python",
            "subtitles_translator/cli.py",
            "-i",
            "tests/test_cli.srt",
            "-o",
            "tests/test_translated.srt",
            "-s",
            "en",
            "-t",
            "fr",
        ]
    )
    with open("tests/test_translated.srt", encoding="utf-8") as file:
        content = file.read().splitlines()
        assert content[2] == "Bonjour le monde!"
