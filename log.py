import os
import sys
from datetime import datetime

def escrever_log(mensagem: str):
    # Detecta o caminho real (do .exe ou do script)
    if getattr(sys, 'frozen', False):
        pasta_base = os.path.dirname(sys.executable)
    else:
        pasta_base = os.path.dirname(os.path.abspath(__file__))

    caminho_log = os.path.join(pasta_base, "log.txt")

    # Timestamp atual no formato: 2025-07-28 15:30:45
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escreve a mensagem com timestamp
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem}\n")
