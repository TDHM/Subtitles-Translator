# Neural Subtitles Translator

[![Release](https://img.shields.io/github/v/release/tdhm/subtitles-translator)](https://img.shields.io/github/v/release/tdhm/subtitles-translator)
[![Build status](https://img.shields.io/github/actions/workflow/status/tdhm/subtitles-translator/main.yml?branch=main)](https://github.com/tdhm/subtitles-translator/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/tdhm/subtitles-translator/branch/main/graph/badge.svg)](https://codecov.io/gh/tdhm/subtitles-translator)
[![Commit activity](https://img.shields.io/github/commit-activity/m/tdhm/subtitles-translator)](https://img.shields.io/github/commit-activity/m/tdhm/subtitles-translator)
[![License](https://img.shields.io/github/license/tdhm/subtitles-translator)](https://img.shields.io/github/license/tdhm/subtitles-translator)

Automatic subtitles translation with a local neural machine translation model. No third-party service required: the translation is done locally with small but efficient neural network models.

Original movie in French            |  Output of automatic translation
:-------------------------:|:-------------------------:
![](./img/bon_voyage_fr.png)  |  ![](./img/bon_voyage_en.png)

### Installation

Subtitles Translator is available as [`subtitles_translator`](https://pypi.org/project/subtitles-translator/) on PyPI:

```shell
pip install subtitles_translator
```

You'll also need to install [`ffmpeg`](https://ffmpeg.org/), which is available from most package managers:

```shell
# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg
```

### Usage

With the following command, subtitles from 'video.mp4' will be extracted and translated from 'french' to 'english' and added to 'video.mp4' as a new subtitles track:

```shell
subtitles_translator -i video.mp4 -s fr -t en
```