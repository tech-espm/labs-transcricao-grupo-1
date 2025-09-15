from fastapi import FastAPI
from fastapi.responses import JSONResponse
from audio_lab import transcribe_with_timestamps
from leitura_json import objs

app = FastAPI(title="API de Transcrição de Áudio", version="0.1")

def generate_JSON():
    word_timings = transcribe_with_timestamps()
    return JSONResponse(content={word_timings})


@app.get("/")
def word_timings():
    return transcribe_with_timestamps()

def generate_phrase_number(n):
    output = []
    for obj in objs:
        if len(output) == n:
            print(output)
            output.clear()
            output.append(obj["word"])
        else:
            output.append(obj["word"])
    if len(output) < 5:
        print(output)