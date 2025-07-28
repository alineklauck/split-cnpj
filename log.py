import os
from datetime import datetime

def escrever_log(mensagem: str):
    # Caminho absoluto para log.txt na mesma pasta do script
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    caminho_log = os.path.join(pasta_script, "log.txt")

    # Timestamp atual no formato: 2025-07-28 15:30:45
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Escreve a mensagem com timestamp
    with open(caminho_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem}\n")
