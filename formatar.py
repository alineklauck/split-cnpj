import os
import pandas as pd
import json
import re
import sys
from log import escrever_log as log

def processar_xlsx(nome_arquivo, path_saida_json='bd.json'):
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(diretorio, nome_arquivo)

    # Força leitura do cabeçalho correto
    planilhas = pd.read_excel(caminho_completo, sheet_name=None)

    resultados = []

    for nome_planilha, df in planilhas.items():
        colunas_necessarias = {'Turma', 'Pasta', 'Coluna1', 'Cartório', 'Emails'}
        if colunas_necessarias.issubset(df.columns):
            df = df.rename(columns={'Coluna1': 'CNPJ', 'Cartório': 'Nome'})

            df['Caminho'] = df.apply(lambda row: f"Turma {row['Turma']}/{row['Pasta']}", axis=1)
            df_resultado = df[['CNPJ', 'Caminho', 'Nome', 'Emails']]
            resultados.extend(df_resultado.to_dict(orient='records'))
        else:
            print(f"A planilha '{nome_planilha}' não contém todas as colunas necessárias.")
            log(f"A planilha '{nome_planilha}' não contém todas as colunas necessárias.")

    if resultados:
        saida_completa = os.path.join(diretorio, path_saida_json)
        with open(saida_completa, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"Arquivo JSON salvo como: {saida_completa}")
        log(f"Arquivo JSON salvo como: {saida_completa}")
    else:
        print("Nenhuma planilha válida encontrada.")
        log("Nenhuma planilha válida encontrada.")

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_cnpj(cnpj):
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def identificar_documento(s):
    # Extrai apenas os números
    numeros = re.sub(r'\D', '', s)

    if "0001" in numeros:
        cnpj = numeros.zfill(14)
        return f"{formatar_cnpj(cnpj)}"
    else:
        cpf = numeros.zfill(11)
        return f"{formatar_cpf(cpf)}"

def buscar_caminho(cnpj: str) -> str | None:
    try:
        if getattr(sys, 'frozen', False):
            # Executável
            pasta_do_exe = os.path.dirname(sys.executable)
        else:
            # Script Python
            pasta_do_exe = os.path.dirname(os.path.abspath(__file__))

        caminho_json = os.path.join(pasta_do_exe, 'bd.json')

        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        for item in dados:
            if item.get("CNPJ") == cnpj:
                return item.get("Caminho")

    except FileNotFoundError:
        print(f"Arquivo '{caminho_json}' não encontrado.")
        log(f"Arquivo '{caminho_json}' não encontrado.")
    except json.JSONDecodeError:
        print(f"Erro ao ler o conteúdo de '{caminho_json}'.")
        log(f"Erro ao ler o conteúdo de '{caminho_json}'.")
    return None

if __name__ == "__main__":
    print("Insira o nome do arquivo")
    processar_xlsx((input(),".xlsx"))
    #print(identificar_documento("cliente 000100"))
    #print(identificar_documento("cpf do cliente é 123456789"))
    #print(buscar_caminho("00.000.000/0001-00"))