import os
import re
import shutil
import stat
from formatar import identificar_documento, buscar_caminho
from log import escrever_log as log

def remover_somente_leitura(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)

base_path = r"C:\Users\***\Certificados - Documentos"
save_path = "C:/oi/"

for nome in os.listdir(base_path):
    caminho = os.path.join(base_path, nome)
    if os.path.isdir(caminho) and len(re.findall(r'\d', nome)) >= 6:
        nome_formatado = identificar_documento(str(nome))
        caminho_bd = buscar_caminho(nome_formatado)
        log(("CNPJ/CPF: ", nome_formatado, "|| Caminho: ", caminho_bd))
        if caminho_bd is None:
            continue
        
        caminho_origem = os.path.join(base_path, nome)
        destino = os.path.join(save_path, caminho_bd, "Sharepoint", "Certificados")
        os.makedirs(destino, exist_ok=True)

        arquivos_origem = os.listdir(caminho_origem)
        copiados_com_sucesso = []

        for arquivo in arquivos_origem:
            origem_arquivo = os.path.join(caminho_origem, arquivo)
            destino_arquivo = os.path.join(destino, arquivo)
            if os.path.isfile(origem_arquivo):
                try:
                    shutil.copy2(origem_arquivo, destino_arquivo)
                    if os.path.exists(destino_arquivo):
                        copiados_com_sucesso.append(arquivo)
                except Exception as e:
                    print(f"Erro ao copiar {arquivo}: {e}")
                    log((f"Erro ao copiar {arquivo}: {e}"))

        arquivos_esperados = [f for f in arquivos_origem if os.path.isfile(os.path.join(caminho_origem, f))]

        if sorted(copiados_com_sucesso) == sorted(arquivos_esperados):
            try:
                shutil.rmtree(caminho_origem, onerror=remover_somente_leitura)
                print("Todos os arquivos copiados. Pasta original apagada:", caminho_origem)
                log(("Todos os arquivos copiados. Pasta original apagada:", caminho_origem))
            except Exception as e:
                print(f"Erro ao apagar a pasta {caminho_origem}: {e}")
                log(f"Erro ao apagar a pasta {caminho_origem}: {e}")
        else:
            print(f"Nem todos os arquivos foram copiados. Pasta NÃO foi apagada: {caminho_origem}")
            log(("Nem todos os arquivos foram copiados. Pasta NÃO foi apagada: {caminho_origem}"))

input("Enter para fechar")