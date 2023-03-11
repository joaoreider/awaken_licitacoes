
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

def calcula_header_tabela_cmed(df):

    """ Calcula o header (onde vai começar a ler) da tabela CMED.
    

    Parâmetros: 

        df (pd.dataframe): A tabela CMED
    Retorno:

       (int): header , -1 se deu erro

    """
    colunas = ['SUBSTÂNCIA', 'LABORATÓRIO', 'REGIME DE PREÇO']
    for i in range(len(df)):

        indice = df.iloc[i].values

        resultado = 0
        try:
            for palavra in indice:
                if palavra in colunas:
                    resultado += 1
            if resultado == 3:   
                return i+1
        except:
            #raise Exception('N foi possível converter indice para lista')
            return -1

