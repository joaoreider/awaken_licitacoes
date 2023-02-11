
import os
import pandas as pd
from tratar_planilha import preco_unitario_tabela_cmed
from tratar_proposta import tratar_proposta_excel_md

# Encontrar o nome da planilha mais recente
lista_de_planilhas = os.listdir("downloads")
# remover um arquivo gerado pelo python que começa com .~lock
lista_de_planilhas = [x for x in lista_de_planilhas if 'lock' not in x]
print('l: ', lista_de_planilhas)

ultima_planilha = max(lista_de_planilhas, key=lambda x: os.path.getctime(os.path.join("downloads/", x)))

# Leitura da planilha (header para ler a partir da linha 46 (onde começa a tabela))
print(ultima_planilha)
df1 = pd.read_excel(os.path.join("downloads", ultima_planilha), header=46)

# colunas manter: subs, labo, regis, apres, pf 18%
df1 = df1[['SUBSTÂNCIA', 'LABORATÓRIO', 'REGISTRO', 'APRESENTAÇÃO', 'PF 18%']] 

tabela = preco_unitario_tabela_cmed(df1)
proposta_ok, proposta, _ = tratar_proposta_excel_md('propostas/simões filho.xls')

