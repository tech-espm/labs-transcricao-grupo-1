import openai
import json
from config import api_key
 
# Para criar o mockup
 
client = openai.OpenAI
 
with open("WhatsApp Ptt 2025-08-18 at 15.30.03.ogg", "rb") as audio_file:
	transcript = client.audio.transcriptions.create(
		model="whisper-1",
		file=audio_file,
		response_format="verbose_json",
		timestamp_granularities=["word"]
	)
 
with open("teste.json", "w", encoding="utf-8") as arquivo_json:
	lista = []
	for word in transcript.words:
		lista.append({
			"start": word.start,
			"end": word.end,
			"word": word.word
		});
	arquivo_json.write(json.dumps(lista))