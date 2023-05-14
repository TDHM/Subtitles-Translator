!!! note
    Please note that the current version only supports MP4 video files (MKV support coming soon).
    Your MP4 must contain only one subtitles track, which will be translated and replaced in a new MP4 file.

!!! note
    You will have to use codes to specify source and target languages.
    You can find them here: [Available Languages](available_languages.md).
    Complete CLI reference is available here: [CLI reference](cli_reference.md)

## MP4 to MP4

With the following command, subtitles from *video.mp4* will be extracted and translated from *french* to *english*. The video containing translated subtitles will be saved as *translated_video.mp4*:

```shell
subtitles_translator -i video.mp4 -o translated_video.mp4 -s fr -t en
```

## MP4 to SRT

With the following command, subtitles from *video.mp4* will be extracted and translated from *french* to *english*. Translated subtitles will be saved as *translated.srt*.

```shell
subtitles_translator -i video.mp4 -o translated.srt -s fr -t en
```

## SRT to SRT

With the following command, subtitles contained in the SRT file *source.srt* will be translated from *french* to *english*. Translated subtitles will be saved as *translated.srt*.

```shell
subtitles_translator -i source.srt -o translated.srt -s fr -t en
```