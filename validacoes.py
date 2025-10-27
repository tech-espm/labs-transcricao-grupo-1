from flask import request
from dotenv import load_dotenv
import os

load_dotenv()

# --- Configurações ---
EXTENSOES_PERMITIDAS = {'.ogg', '.wav', '.mp3', '.m4a', '.webm'}
TAMANHO_MAX_MB = 25


def validar_arquivo_audio():
    arquivo = request.files.get('audio')

    if not arquivo:
        return False, "Arquivo de áudio não enviado", 400

    if not arquivo.filename:
        return False, "Nenhum arquivo selecionado", 400

    nome = arquivo.filename.lower()
    if not any(nome.endswith(ext) for ext in EXTENSOES_PERMITIDAS):
        return False, "Tipo de arquivo não é compatível", 415

    # Verificação de tamanho
    arquivo.seek(0, os.SEEK_END)
    tamanho = arquivo.tell()
    arquivo.seek(0)

    if tamanho == 0:
        return False, "Arquivo vazio", 400
    if tamanho > TAMANHO_MAX_MB * 1024 * 1024:
        return False, f"Arquivo muito grande (máximo {TAMANHO_MAX_MB}MB)", 413

    return True, arquivo, 200


def validar_chave_api():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        return False, "API key não configurada", 500

    return True, api_key, 200
