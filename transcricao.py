from openai import OpenAI
from dotenv import load_dotenv
import os 

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
audio_file = open("WhatsApp Ptt 2025-08-18 at 15.30.03.ogg", "rb")

translation = client.audio.translations.create(
    model="whisper-1", 
    file=audio_file,
)

print(translation.text)