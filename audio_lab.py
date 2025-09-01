from openai import OpenAI
from config import api_key
import whisper

model = whisper.load_model("medium")

result = model.transcribe("escopo.ogg", language="pt")

with open("transcricao.txt", "w", encoding="utf-8") as file:
    file.write(result["text"])

client = OpenAI(api_key=api_key)
audio_file= open("WhatsApp Ptt 2025-08-18 at 15.30.03.ogg", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)