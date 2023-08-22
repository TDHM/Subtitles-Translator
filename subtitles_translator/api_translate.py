from subtitles_translator.translator_gcp import Translator

from fastapi import FastAPI
from pydantic import BaseModel

class SourceText(BaseModel):
    text: str = ""

app = FastAPI()

@app.on_event("startup")
def load_model():
    print("initializing translator...")
    translator = Translator()
    print("done")

@app.get("/")
def read_root():
    return {"Hello": "World"}

# response = requests.get("http://localhost:8000/translate/", json={"text":"Hello world!"})
@app.get("/translate")
def translate(source_text: SourceText = None):
    translated_text = translator.translate(source_text.text)
    return translated_text