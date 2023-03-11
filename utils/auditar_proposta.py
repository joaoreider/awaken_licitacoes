
import os
import pandas as pd
from tratar_planilha import preco_unitario_tabela_cmed, calcula_header_tabela_cmed
from tratar_proposta import tratar_proposta_excel_md
from funcoes import *

# Encontrar o nome da planilha mais recente
lista_de_planilhas = os.listdir("downloads")
# remover um arquivo gerado pelo python que começa com .~lock
lista_de_planilhas = [x for x in lista_de_planilhas if 'lock' not in x]
print('l: ', lista_de_planilhas)

ultima_planilha = max(lista_de_planilhas, key=lambda x: os.path.getctime(os.path.join("downloads/", x)))

# Leitura da planilha (header para ler a partir da linha 46 (onde começa a tabela))
print('PLANILHA MAIS RECENTE:', ultima_planilha)

tabela_calcular_header = pd.read_excel(os.path.join("downloads", ultima_planilha))
header = calcula_header_tabela_cmed(tabela_calcular_header)
#print(header)
df1 = pd.read_excel(os.path.join("downloads", ultima_planilha), header=header)


# colunas manter: subs, labo, regis, apres, pf 18%
df1 = df1[['SUBSTÂNCIA', 'LABORATÓRIO', 'REGISTRO', 'APRESENTAÇÃO', 'PF 18%']] 

tabela = preco_unitario_tabela_cmed(df1)
nome_proposta = 'simões filho.xls'
proposta_ok, proposta, _ = tratar_proposta_excel_md(os.path.join("propostas", nome_proposta))

if proposta_ok:
    
    # resultado: 
    resultado = {}
    registros = []
    descricao_proposta = []
    apresentacao_tabela = []
    laboratorio = []
    situacao_marca = []
    situacao_preco = []


    def registro_incompleto(registro, descricao):

        apresentacao_tabela.append('registro incompleto')
        laboratorio.append('registro incompleto')
        situacao_marca.append('registro incompleto')
        situacao_preco.append('registro incompleto')

    # pegar o registro (se tiver 13 digitos)
    # buscar o registro na tabela
    # comparar a marca 
    # comparar o preco
    for i in range(len(proposta)):

        # Inicializa as variáveis da proposta (registro e descricao)
        item_proposta = proposta.iloc[i]
        registro = item_proposta['Registros']
        registros.append(registro)
        descricao = item_proposta['Descrição do Item']
        descricao_proposta.append(descricao)

        #Só audita o registro com 13 dititos (completo)
        if len(str(registro)) == 13:
            
            item_tabela = tabela[tabela['REGISTRO'] == str(registro)]
            # len > 0 achou o registro
            if len(item_tabela) > 0:

                marca_proposta = item_proposta['Marca']
                marca_tabela = item_tabela['LABORATÓRIO'].values[0]
                laboratorio.append(marca_tabela)

                descricao_tabela = item_tabela['APRESENTAÇÃO'].values[0]
                apresentacao_tabela.append(descricao_tabela)
                
                marca_valida = comparar_marca(marca_proposta, marca_tabela)
                situacao_marca.append(marca_valida)

                # Marca ok compara o preço
                if marca_valida:
                    preco_tabela = item_tabela['preco_unitario_ba'].values[0]
                    preco_proposta = item_proposta['Preço Unitário']
                    try: 
                        preco_proposta = float(preco_proposta)
                        preco_tabela = float(preco_tabela)
                        preco_valido = comparar_preco(preco_tabela=preco_tabela, preco_proposta=preco_proposta)
                        situacao_preco.append(preco_valido)
                    except:
                        situacao_preco.append('indisponivel')
                
                # marca errada nao compara preco
                else:
                    situacao_preco.append('marca errada')


        # registro incompleto: nao da pra auditar
        else:
            registro_incompleto(registro=registro, descricao=descricao)
        

        

    # Monto o dataframe de resultados
    resultado['registro'] = registros
    resultado['descricao_da_proposta'] = descricao_proposta
    resultado['descricao_da_tabela'] = apresentacao_tabela
    resultado['laboratorio'] = laboratorio
    resultado['situacao_da_marca'] = situacao_marca
    resultado['situacao_do_preco'] = situacao_preco

    #print(resultado)

    # Monta o dataframe
    try:
        df_final = pd.DataFrame(resultado)
        #print(df_final)
    except: raise Exception('N foi possível montar o dataframe')

    # Exporta para excel

    try: 
        formato = nome_proposta.split('.')[-1]
        nome_proposta = nome_proposta.replace(formato, 'csv')
        df_final.to_csv(os.path.join("resultados", 'resultado_'+nome_proposta), sep=';', encoding = 'utf-8', index =False)
    except: raise Exception('N foi possível exportar o dataframe para csv')


