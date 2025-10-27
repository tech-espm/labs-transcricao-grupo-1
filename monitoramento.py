from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from collections import deque
from datetime import datetime, timedelta
from flask import Response
import threading

# --- Contadores Prometheus ---
UPLOADS_VALIDOS = Counter("uploads_validos_total", "Uploads que passaram na validação")
PROCESSAMENTOS_OK = Counter("processamentos_ok_total", "Uploads válidos processados com sucesso")
PROCESSAMENTOS_ERRO = Counter("processamentos_erro_total", "Uploads válidos com erro no processamento")

# --- Estruturas de controle ---
_EVENTOS = deque()  
_LOCK = threading.Lock()
_JANELA_HORAS = 24


# --- Funções auxiliares ---
def _limpar_eventos_antigos():
    limite = datetime.utcnow() - timedelta(hours=_JANELA_HORAS)
    while _EVENTOS and _EVENTOS[0][0] < limite:
        _EVENTOS.popleft()


def _registrar_evento(valido=True, sucesso=None):
    with _LOCK:
        _EVENTOS.append((datetime.utcnow(), valido, sucesso))
        _limpar_eventos_antigos()


# --- Funções principais ---
def registrar_upload_valido():
    _registrar_evento(valido=True)
    UPLOADS_VALIDOS.inc()


def registrar_processamento(sucesso: bool):
    _registrar_evento(valido=True, sucesso=sucesso)
    (PROCESSAMENTOS_OK if sucesso else PROCESSAMENTOS_ERRO).inc()


def taxa_sucesso_24h():
    with _LOCK:
        _limpar_eventos_antigos()
        processados = [e for e in _EVENTOS if e[2] is not None]
        if not processados:
            return 1.0
        ok = sum(1 for _, _, s in processados if s)
        return ok / len(processados)


def resumo_24h():
    with _LOCK:
        _limpar_eventos_antigos()
        validos = sum(1 for _, v, s in _EVENTOS if v and s is None)
        processados = [e for e in _EVENTOS if e[2] is not None]
        ok = sum(1 for _, _, s in processados if s)
        erro = len(processados) - ok

    return {
        "validos_registrados": validos,
        "processamentos_total": len(processados),
        "processamentos_ok": ok,
        "processamentos_erro": erro,
        "taxa_sucesso_24h": round(taxa_sucesso_24h(), 4),
    }


def metricas_endpoint():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
