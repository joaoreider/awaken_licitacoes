
from funcoes import pegar_quantidade_da_apresentacao

def preco_unitario_tabela_cmed(df):

    """ Calcula o preco unitario do item na tabela CMED.
    

    Parâmetros: 

        df (pd.dataframe): A tabela CMED que terá o campo preço_unitario calculado
    Retorno:

       (pd.Dataframe): Tabela com o preço unitário calculado

    """

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

    return df



