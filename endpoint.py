from flask import Flask, jsonify, request
import os
from monitoramento import registrar_upload_valido, registrar_processamento
from validacoes import validar_arquivo_audio
from openai import OpenAI
import tempfile

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
AUDIO_MODEL = "whisper-1"  

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    
    sucesso, resultado, status = validar_arquivo_audio()
    if not sucesso:
        return jsonify({"erro": resultado}), status
    
    arquivo_request = resultado

    registrar_upload_valido()

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(arquivo_request.filename)[1]) as tmp:
            arquivo_request.save(tmp.name)
            temp_path = tmp.name

        with open(temp_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model=AUDIO_MODEL,
                file=f
            )
        
        registrar_processamento(True)
        return jsonify({"transcricao": transcription.text}), 200

    except Exception as e:
        registrar_processamento(False)
        return jsonify({"erro": f"Falha no processamento: {str(e)}"}), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(debug=True)