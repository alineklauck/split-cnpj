import json
from collections import Counter
import os
from log import escrever_log as log

# Caminho para o arquivo JSON
pasta_do_script = os.path.dirname(os.path.abspath(__file__))
arquivo = os.path.join(pasta_do_script, 'bd.json')

# Lê o conteúdo do arquivo
with open(arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Extrai os CNPJs
cnpjs = [item.get("CNPJ") for item in dados if "CNPJ" in item]

# Conta as ocorrências
contador = Counter(cnpjs)

# Filtra os duplicados
duplicados = {cnpj: count for cnpj, count in contador.items() if count > 1}

# Resultado
if duplicados:
    print("CNPJs duplicados encontrados:")
    log("CNPJs duplicados encontrados:")
    for cnpj, vezes in duplicados.items():
        print(f"CNPJ {cnpj} aparece {vezes} vezes.")
        log(f"CNPJ {cnpj} aparece {vezes} vezes.")
else:
    print("Nenhum CNPJ duplicado encontrado.")
    log("Nenhum CNPJ duplicado encontrado.")
