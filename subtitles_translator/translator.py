from __future__ import annotations

from typing import Generator, Iterable

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer  # type: ignore  # noqa: PGH003

from subtitles_translator.available_languages import AvailableLanguages
from subtitles_translator.subtitles import Subtitles


class Translator:
    def __init__(
        self,
        source_language: AvailableLanguages,
        target_language: AvailableLanguages,
    ) -> None:
        """This class defines and stores a language model (such as MarianMT) for the translation
        task, from source_language to target_language. It also provides functions to perform full
        translations effectively from extracted subtitles.

        Args:
            source_language (AvailableLanguages, optional): language of the source subtitles.
            target_language (AvailableLanguages, optional): target language.
        """
        self.source_language = source_language
        self.target_language = target_language

        model_name = f"Helsinki-NLP/opus-mt-{source_language.value}-{target_language.value}"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def translate(self, input_text: str) -> str:
        """Translate a text input using the model.

        Args:
            input_text (str): text to be translated (usually, a single sentence)

        Returns:
            str: translated text.
        """

        batch = self.tokenizer([input_text], return_tensors="pt")
        generated_ids = self.model.generate(**batch)
        translated_text = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return translated_text  # type: ignore  # noqa: PGH003

    def translate_subtitles(self, subtitles: Subtitles) -> None:
        """Use given translator to perform translation using dictionary of aggregated
        subtitles lines. Each translated line replaces the original one in the full_text_line
        list created at the beginning of the process.

        Args:
            subtitles (subtitles object): object of the Subtitles class.
        """
        # here the iterable is aggregated_dico_lines.items(), we use progressBar
        for full_line_text, lines_ranges in self.progressBar(
            iterable=subtitles.aggregated_dico_lines.items(), prefix="Progress:", suffix="Complete", length=50
        ):
            line_text = full_line_text.replace("\n", "")
            translated_text = self.translate(line_text)
            for line_pos in lines_ranges:
                # case when the current screen subtitles stands on 1 line
                if len(line_pos) == 1:
                    subtitles.full_text_lines[line_pos[0]] = translated_text
                # case when we're on two lines subtitles
                # we try to "rebuild" two-line subtitles
                if len(line_pos) == 2:
                    split_text = translated_text.split(" ")
                    mid_line = len(split_text) // 2
                    first_line = " ".join(split_text[:mid_line])
                    second_line = " ".join(split_text[mid_line:])
                    subtitles.full_text_lines[line_pos[0]] = first_line
                    subtitles.full_text_lines[line_pos[1]] = second_line

    @staticmethod
    def progressBar(
        iterable: Iterable[tuple[str, list]],
        prefix: str = "",
        suffix: str = "",
        decimals: int = 1,
        length: int = 100,
        fill: str = "█",
        printEnd: str = "\r",
    ) -> Generator[tuple[str, list], None, None]:
        """
        Call in a loop to create terminal progress bar.
        Source : https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters/13685020

        Args:
            iterable (Iterable): iterable object
            prefix (str, optional): prefix string
            suffix (str, optional): suffix string
            decimals (int, optional): positive number of decimals in percent complete
            length (int, optional) : character length of bar
            fill (str, optional): bar fill character (Str)
            printEnd (str, optional): end character (e.g. "\r", "\r\n")
        """
        total = len(iterable)  # type: ignore # type checks fails here (len of iterable ?)  # noqa: PGH003
        # Progress Bar Printing Function
        def printProgressBar(iteration: int) -> None:
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + "-" * (length - filledLength)
            print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)

        # Initial Call
        printProgressBar(0)
        # Update Progress Bar
        for i, item in enumerate(iterable):
            yield item
            printProgressBar(i + 1)
        # Print New Line on Complete
        print()
