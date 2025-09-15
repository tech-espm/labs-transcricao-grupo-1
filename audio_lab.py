from openai import OpenAI
from config import api_key

client = OpenAI(api_key=api_key)

def transcribe_with_timestamps():
    audio_path = "WhatsApp Ptt 2025-08-18 at 15.30.03.ogg"
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return [
        {
            "start": word,
            "end": word,
            "word" : word
        }
        for word in transcription.words
    ]