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
