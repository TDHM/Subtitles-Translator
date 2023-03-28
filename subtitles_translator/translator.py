from enum import Enum
from typing import Generator, no_type_check

from subtitles import Subtitles
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class AvailableLanguages(Enum):
    english = "en"
    french = "fr"


class Translator:
    def __init__(
        self,
        source_language: AvailableLanguages = AvailableLanguages.english,
        target_language: AvailableLanguages = AvailableLanguages.french,
    ) -> None:
        """This class defines and stores a language model (such as MarianMT) for the translation
        task, from source_language to target_language. It also provides functions to perform full
        translations effectively from extracted subtitles.


        Args:
            source_language (AvailableLanguages, optional): language of the source subtitles. Defaults to "en".
            target_language (AvailableLanguages, optional): target language. Defaults to "fr".
        """
        self.source_language = source_language
        self.target_language = target_language

        self.tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-fr")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-fr")

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

        return translated_text

    def translate_subtitles(self, subtitles: Subtitles) -> None:
        """Use given translator to perform translation using dictionary of aggregated
        subtitles lines. Each translated line replaces the original one in the full_text_line
        list created at the beginning of the process.

        Args:
            subtitles (subtitles object): object of the Subtitles class.
        """
        for full_line_text, line_pos in self.progressBar(
            iterable=subtitles.aggregated_dico_lines.items(), prefix="Progress:", suffix="Complete", length=50
        ):
            line_text = full_line_text.replace("\n", "").replace("â™ª", "")
            translated_text = self.translate(line_text)
            if len(line_pos) == 1:
                subtitles.full_text_lines[line_pos[0]] = translated_text
            if len(line_pos) == 2:
                split_text = translated_text.split(" ")
                mid_line = len(split_text) // 2
                first_line = " ".join(split_text[:mid_line])
                second_line = " ".join(split_text[mid_line:])
                subtitles.full_text_lines[line_pos[0]] = first_line
                subtitles.full_text_lines[line_pos[1]] = second_line

    @no_type_check
    @staticmethod
    def progressBar(
        iterable: list[tuple[str, list]],
        prefix: str = "",
        suffix: str = "",
        decimals: int = 1,
        length: int = 100,
        fill: str = "█",
        printEnd: str = "\r",
    ) -> Generator[tuple[str, list], None, None]:
        """
        Call in a loop to create terminal progress bar
        @params:
            iterable    - Required  : iterable object (Iterable)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

        Source : https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters/13685020
        """
        total = len(iterable)  # type checks fails here (len of iterable ?)
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
