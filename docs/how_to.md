### Usage

Please note that the current version only supports MP4 video files (MKV support coming soon).
Your MP4 must contain only one subtitles track, which will be translated and replaced in a new MP4 file.
You can also translates SRT subtitles files, or extract and translate SRT files from a MP4 (look at the doc!).

With the following command, subtitles from 'video.mp4' will be extracted and translated from 'french' to 'english'. The video containing translated subtitles will be saved as 'translated_video.mp4':

```shell
subtitles_translator -i video.mp4 -o translated_video.mp4 -s fr -t en