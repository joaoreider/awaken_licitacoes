
import os
import pandas as pd

# Encontrar o nome da planilha mais recente
lista_de_planilhas = os.listdir("downloads")
print(lista_de_planilhas)
ultima_planilha = max(lista_de_planilhas, key=lambda x: os.path.getctime(os.path.join("downloads/", x)))

# Leitura da planilha

df = pd.read_excel(os.path.join("downloads", ultima_planilha))
print(df.head())


# TODO: manipular a planilha para ficar só a tabela (ver se é necessário isso)