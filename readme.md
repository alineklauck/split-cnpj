# Split cnpj

Ferramenta para separação de certificados de acordo com o banco de dados

- Os certificados são todos salvos dentro de uma mesma pasta raiz.
- Dependendo do formulário, podem ser separados de acordo com o CPJ/CPF ou nome.
- Esse código serve pra CNPJ/CPF, ou pode ser alterado para identificar outra forma padronizada de separação.

## Setup

A linha 12 do arquivo pastas.py deve ser alterada, especificando o caminho correto para a raiz das pastas a serem separadas.
Recomenda-se que a linha 13, se alterada, aponte para uma pasta local fora do oneDrive.

```sh
base_path = r"C:\raiz do problema"
save_path = "C:/output/"
```

Deve ser gerado um banco de dados, se não existir. Executar diretamente o formatar.py irá permitir extrair de um arquivo xlsx.

O arquivo xlsx será lido da seguinte forma:
- Cada aba será considerada uma planilha
- O cabeçalho de todas as planilhas devem estar na primeira linha

É necessário existir as colunas:
- Turma (Apenas o nome da turma, sem a palavra "Turma")
- Pasta (O nome da pasta do cartório dentro da turma correspondente)
- Coluna1 (CNPJ)
- Cartório (O nome do titular)
- Emails (E-mail do responsável)

Caso esteja tudo certo, o arquivo **db.json** será criado, caso contrário o programa retornará uma mensagem de erro.

## Uso

Execute o pastas.py e acompanhe o processo pelo prompt de comando.

O programa escaneia todas as pastas dentro de **base_path**. Caso o nome da pasta tenha pelo menos 6 números, irá limpar e tentar formatar como CNPJ (Se existir "0001" na string) ou CPF. Irá cruzar o nome com a base de dados, procurando a entrada correspondente.

Pastas não encontradas serão explicitadas apenas no arquivo de log.
Caso exista uma entrada correspondente, antes de ser excluida a pasta original, os arquivos serão copiados seguindo a estrutura:
```save_path/Turma {Turma + Pasta}/Sharepoint/Certificados```

a.py serve pra verificar se o banco de dados não tem CNPJ duplicados
