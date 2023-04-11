from __future__ import annotations


class Subtitles:
    def __init__(self, raw_subtitles: list[str], sub_format: str = "srt") -> None:
        """From a raw FFmpeg extraction, process the text and translate it using a given
        Translator object.

        Args:
            raw_subtitles (list[str]): subtitles line by line
            sub_format (str, optional): sub_format of the extracted subtitles. Defaults to "srt".
        """
        self.raw_subtitles = raw_subtitles
        self.sub_format = sub_format

        self.full_text_lines: list[str] = []

        self.aggregated_text_lines: list[str] = []
        self.aggregated_dico_lines: dict[str, list[list]] = {}

        self.build_aggregated_dico()

    def build_aggregated_dico(self) -> None:
        """After converting raw extraction to list of lines, aggregates and clean lines
        in order to be able to translate them. When two lines are combined, both indexes
        are saved in order to replace each line at the end.
        """
        seen_i = set()
        n = len(self.raw_subtitles)

        for i, line in enumerate(self.raw_subtitles):
            self.full_text_lines.append(line)
            if i in seen_i or "-->" in line:
                continue
            agg_line = ""
            if i < n - 1 and self.raw_subtitles[i + 1] == "":
                agg_line += line
                seen_i.add(i)
                self.aggregated_text_lines.append(agg_line)
                if agg_line in self.aggregated_dico_lines:
                    self.aggregated_dico_lines[agg_line].append([i])
                else:
                    self.aggregated_dico_lines[agg_line] = [[i]]
            # the following condition means that we are on the second part of a two lines subtitle text
            if i > 0 and i < n - 2 and self.raw_subtitles[i + 2] == "" and self.raw_subtitles[i - 1] != "":
                seen_i.add(i)
                seen_i.add(i + 1)
                agg_line += line + " " + self.raw_subtitles[i + 1]
                self.aggregated_text_lines.append(self.raw_subtitles[i + 1])
                if agg_line in self.aggregated_dico_lines:
                    self.aggregated_dico_lines[agg_line].append([i, i + 1])
                else:
                    self.aggregated_dico_lines[agg_line] = [[i, i + 1]]

    def save_srt(self, path: str = "translated.srt") -> None:
        """Save current subtitles into an srt files.
        If translate_subtitles was called before, this results in a translated srt file.

        Args:
            path (str, optional): path to the target srt file. Defaults to "translated.srt".
        """
        with open(path, "w", encoding="utf-8") as file:
            for line in self.full_text_lines:
                # in Python we need to write blank lines manually (those in full_text_lines are skipped by default)
                if line == "":
                    file.write("\n")
                else:
                    file.write(line)
                    file.write("\n")
