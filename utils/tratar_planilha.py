
import os
import pandas as pd
from funcoes import pegar_quantidade_da_apresentacao

# Encontrar o nome da planilha mais recente
lista_de_planilhas = os.listdir("downloads")
# remover um arquivo gerado pelo python que começa com .~lock
lista_de_planilhas = [x for x in lista_de_planilhas if 'lock' not in x]
print('l: ', lista_de_planilhas)

ultima_planilha = max(lista_de_planilhas, key=lambda x: os.path.getctime(os.path.join("downloads/", x)))

# Leitura da planilha (header para ler a partir da linha 46 (onde começa a tabela))
print(ultima_planilha)
df = pd.read_excel(os.path.join("downloads", ultima_planilha), header=46)


# colunas manter: subs, labo, regis, apres, pf 18%
df = df[['SUBSTÂNCIA', 'LABORATÓRIO', 'REGISTRO', 'APRESENTAÇÃO', 'PF 18%']] 

# coletando as quantidades do item de cada apresentacao
apresentacoes = df['APRESENTAÇÃO'].values
quant = []
for i in apresentacoes:
    quant.append(pegar_quantidade_da_apresentacao(i))

df['quantidade'] = quant


# Calculando o preco unitário de cada item
preco_unit = []
for i, preco in enumerate(df['PF 18%']):

    quantidade = df['quantidade'].iloc[i]

    if quantidade != -1:

        try: 
            
            aux = float(str(preco).replace(',', '.')) / int(quantidade)
            preco_unit.append(aux)

        except:
            preco_unit.append('indisponivel')
    else:

        preco_unit.append('indisponivel')

df['preco_unitario_ba'] = preco_unit

print(df[['APRESENTAÇÃO', 'quantidade', 'preco_unitario_ba']].head(20))

