from fastapi import FastAPI
from pydantic import BaseModel

from subtitles_translator.translator_gcp import Translator


class SourceText(BaseModel):
    text: str = ""


translator = Translator()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# response = requests.get("http://localhost:8000/translate/", json={"text":"Hello world!"})
# curl -X GET localhost:8000/translate -H 'Content-Type: application/json' -d '{"text":"Hello world!"}'
@app.get("/translate")
def translate(source_text: SourceText = None):
    translated_text = translator.translate(source_text.text)
    return translated_text
