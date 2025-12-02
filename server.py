import os
from flask import Flask, request, jsonify
import openai
import json
import config
from config import api_key

client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)


@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    audio_file = request.files["file"]

    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )

    lista = []
    for word in transcript.words:
        lista.append({
            "start": word.start,
            "end": word.end,
            "word": word.word
        })

    resposta = {
        "text": transcript.text,
        "words": lista
    }

    return jsonify(resposta)


if __name__ == "__main__":
    app.run(host=config.host, port=config.port)