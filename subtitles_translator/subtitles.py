class Subtitles:
    def __init__(self, raw_subtitles: str, sub_format: str = "srt") -> None:
        """From a raw FFmpeg extraction, process the text and translate it using a given
        Translator object.

        Args:
            raw_subtitles (str): subtitles in the given format.
            sub_format (str, optional): sub_format of the extracted subtitles. Defaults to "srt".
        """
        self.raw_subtitles = raw_subtitles
        self.sub_format = sub_format

        self.text_lines = []
        self.dico_lines = {}
        self.full_text_lines = []

        self.aggregated_text_lines = []
        self.aggregated_dico_lines = {}

        self.process_timestamps()
        self.build_aggregated_dico()

    def process_timestamps(self) -> None:
        """Filter out timestamps while keeping track of each line index in order to replace
        original text by the translated one at the end of the process.
        """
        for i, line in enumerate(self.raw_subtitles):
            self.full_text_lines.append(line)
            if "-->" not in line:
                self.text_lines.append(line)
                # keep track of the line's index in raw_subtitles
                self.dico_lines[line] = i

    def build_aggregated_dico(self) -> None:
        """After converting raw extraction to list of lines, aggregates and clean lines
        in order to be able to translate them. When two lines are combined, both indexes
        are saved in order to replace each line at the end.
        """
        seen_i = set()
        n = len(self.text_lines)

        for i, line in enumerate(self.text_lines):
            if i in seen_i:
                continue
            agg_line = ""
            agg_dico = []
            if i < n - 1 and self.text_lines[i + 1] == "":
                agg_line += line
                agg_dico.append(self.dico_lines[line])
                seen_i.add(i)
                self.aggregated_text_lines.append(agg_line)
                self.aggregated_dico_lines[agg_line] = agg_dico
            if i > 0 and i < n - 2 and self.text_lines[i + 2] == "" and self.text_lines[i - 1] != "":
                seen_i.add(i)
                seen_i.add(i + 1)
                agg_line += line + " " + self.text_lines[i + 1]
                agg_dico.append(self.dico_lines[line])
                agg_dico.append(self.dico_lines[self.text_lines[i + 1]])
                self.aggregated_text_lines.append(self.text_lines[i + 1])
                self.aggregated_dico_lines[agg_line] = agg_dico

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
