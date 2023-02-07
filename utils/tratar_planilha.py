
import os
import pandas as pd

# Encontrar o nome da planilha mais recente
lista_de_planilhas = os.listdir("downloads")
# remover um arquivo gerado pelo python que começa com .~lock
lista_de_planilhas = [x for x in lista_de_planilhas if 'lock' not in x]
print('l: ', lista_de_planilhas)

ultima_planilha = max(lista_de_planilhas, key=lambda x: os.path.getctime(os.path.join("downloads/", x)))

# Leitura da planilha (header para ler a partir da linha 46 (onde começa a tabela))
print(ultima_planilha)
df = pd.read_excel(os.path.join("downloads", ultima_planilha), header=46)
print(df.head())