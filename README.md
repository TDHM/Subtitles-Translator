# Neural Subtitles Translator

[![Release](https://img.shields.io/github/v/release/tdhm/subtitles-translator)](https://img.shields.io/github/v/release/tdhm/subtitles-translator)
[![Build status](https://img.shields.io/github/actions/workflow/status/tdhm/subtitles-translator/main.yml?branch=main)](https://github.com/tdhm/subtitles-translator/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/tdhm/subtitles-translator/branch/main/graph/badge.svg)](https://codecov.io/gh/tdhm/subtitles-translator)
[![Commit activity](https://img.shields.io/github/commit-activity/m/tdhm/subtitles-translator)](https://img.shields.io/github/commit-activity/m/tdhm/subtitles-translator)
[![License](https://img.shields.io/github/license/tdhm/subtitles-translator)](https://img.shields.io/github/license/tdhm/subtitles-translator)

Automatic subtitles translation with a local neural machine translation model. No third-party service required: the translation is done locally with small but efficient neural network models.

> **Github repository**: <https://github.com/tdhm/subtitles-translator/>

> **Documentation** <https://tdhm.github.io/subtitles-translator/>

Original movie in French            |  Output of automatic translation
:-------------------------:|:-------------------------:
![](./docs/img/bon_voyage_fr.png)  |  ![](./docs/img/bon_voyage_en.png)

> **Note**
> Screenshots are taken from *Bon voyage*, a short French language propaganda film made by Alfred Hitchcock for the British Ministry of Information.
> This film is now in the Public Domain.

### Installation

Subtitles Translator is available as [`subtitles_translator`](https://pypi.org/project/subtitles-translator/) on PyPI:

```shell
pip install subtitles_translator
```

You'll also need to install [`ffmpeg`](https://ffmpeg.org/), which is available from most package managers:

```shell
# on macOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg
```

### Usage

> **Note**
> Please note that the current version only supports MP4 video files (MKV support coming soon).
> Your MP4 must contain only one subtitles track, which will be translated and replaced in a new MP4 file.
> You can also translates SRT subtitles files, or extract and translate SRT files from a MP4 ([look at the doc!](https://tdhm.github.io/subtitles-translator/)).

With the following command, subtitles from 'video.mp4' will be extracted and translated from 'french' to 'english'. The video containing translated subtitles will be saved as 'translated_video.mp4':

```shell
subtitles_translator -i video.mp4 -o translated_video.mp4 -s fr -t en
```