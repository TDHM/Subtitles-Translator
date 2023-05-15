from __future__ import annotations

import pytest

from subtitles_translator.subtitles import Subtitles


@pytest.fixture
def raw_subtitles() -> list[str]:
    raw_str = """
1
00:00:00,498 --> 00:00:02,827
Test 1

2
00:00:02,827 --> 00:00:06,383
Test 2
Test 3

3
00:00:06,383 --> 00:00:09,427
Test 4
"""
    raw_subtitles = raw_str.split("\n")

    return raw_subtitles


@pytest.fixture
def subtitles(raw_subtitles) -> Subtitles:
    subtitles = Subtitles(raw_subtitles)

    return subtitles


def test_build_aggregated_dico(subtitles):
    assert subtitles.full_text_lines[3] == "Test 1"
    assert subtitles.aggregated_dico_lines["Test 1"] == [[3]]
    assert subtitles.aggregated_text_lines[0] == "Test 1"


def test_save_srt(subtitles):
    subtitles.save_srt("test.srt")
    with open("test.srt", encoding="utf-8") as file:
        content = file.read().splitlines()
        assert content[3] == "Test 1"
