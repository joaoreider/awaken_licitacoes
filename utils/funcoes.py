
def pegar_quantidade_da_apresentacao(apresentacao: str) -> int:
    
    """
    Extrai a quantidade do item com base na apresentação.

    Parâmetros: 

        apresentacao (str): A apresentacao do item da tabela CMED.

    Retorno:

       (int): Quantidade extraída da apresentação. Se não achar retorna -1.

    """

    import re
    texto = apresentacao.strip()

    # Padrões da quantidade na apresentação
    padrao_quantidade_no_meio_com_cx = re.compile(r"CX \d{1,3}")
    padrao_quantidade_no_final = re.compile(r" X \d{1,3}$")
    padrao_quantidade_no_meio_com_ct = re.compile(r"CT \d{1,3}")

    # Matches (lista com o retorno do padrão encontrado)
    matches_quantidade_no_meio_com_cx = padrao_quantidade_no_meio_com_cx.findall(texto)
    matches_quantidade_no_final = padrao_quantidade_no_final.findall(texto)
    matches_quantidade_no_meio_com_ct = padrao_quantidade_no_meio_com_ct.findall(texto)


    # Quantidade é o valor do final multiplicado pelo do meio CT: Quantidade = "ct 10 x 2 " =  20
    if len(matches_quantidade_no_final) and len(matches_quantidade_no_meio_com_ct):

        #print(' # Quantidade é o valor do final multiplicado pelo do meio CT: Quantidade = "ct 10 x 2 " =  20')
        quantidade_final = re.sub('[^0-9]', '', matches_quantidade_no_final[0])
        quantidade_meio_ct =  re.sub('[^0-9]', '', matches_quantidade_no_meio_com_ct[0])

        try: 
            return int(quantidade_final) * int(quantidade_meio_ct)
        except:
            return -1
    
    # Quantidade é o valor do final multiplicado pelo do meio CX: Quantidade = "cx 10 x 2 " =  20
    elif len(matches_quantidade_no_final) and len(matches_quantidade_no_meio_com_cx):
        #print('  # Quantidade é o valor do final multiplicado pelo do meio CX: Quantidade = "cx 10 x 2 " =  20')
        quantidade_final = re.sub('[^0-9]', '', matches_quantidade_no_final[0])
        quantidade_meio_cx =  re.sub('[^0-9]', '', matches_quantidade_no_meio_com_cx[0])

        try: 
            return int(quantidade_final) * int(quantidade_meio_cx)
        except:
            return -1
    
    # Quantidade só no final
    elif len(matches_quantidade_no_final) and not (len(matches_quantidade_no_meio_com_ct) or len(matches_quantidade_no_meio_com_cx)):

        #print('# Quantidade só no final')
        quantidade_final = re.sub('[^0-9]', '', matches_quantidade_no_final[0])

        try: 
            return int(quantidade_final)
        except:
            return -1
    
    # Quantidade só no meio com ct
    elif not len(matches_quantidade_no_final) and (len(matches_quantidade_no_meio_com_ct)):
        #print('# Quantidade só no meio com ct')
        quantidade_meio_ct = re.sub('[^0-9]', '', matches_quantidade_no_meio_com_ct[0])

        try: 
            return int(quantidade_meio_ct)
        except:
            return -1
    
    # quantidade só no meio com cx
    elif not len(matches_quantidade_no_final) and (len(matches_quantidade_no_meio_com_cx)):
        
        #print('# quantidade só no meio com cx')
        #print(f' len qtd final: {len(matches_quantidade_no_final)}')
        quantidade_meio_cx = re.sub('[^0-9]', '', matches_quantidade_no_meio_com_cx[0])

        try: 
            return int(quantidade_meio_cx)
        except:
            return -1
    
    # Sem quantidade
    else:
        #print('# Sem quantidade')
        return -1 

def comparar_marca(marca_proposta:str, marca_tabela: str) -> bool:
    
    """
    Compara a marca da proposta com a marca da tabela CMED

    Parâmetros: 

        marca_proposta (str): A marca do item que está na proposta.
        marca_tabela (str): A marca do item que está na tabela.

    Retorno:

    (bool): True se a marca é a mesma False se não.

    """

    from unidecode import unidecode

    texto1 = unidecode(marca_proposta.upper())
    texto2 = unidecode(marca_tabela.upper())

    if texto1 in texto2:
        return True

    return False

def comparar_preco(preco_proposta: float, preco_tabela: float) -> bool:
    
    """
    Compara o preço da proposta com o preço da tabela CMED

    Parâmetros: 

        preço_proposta (str): O preço do item que está na proposta.
        preço_tabela (str): O preço do item que está na tabela.

    Retorno:

    (bool): True se o preço da proposta for menor ou igual ao da tabela False se não.

    """

    if preco_proposta > preco_tabela:
        return False

    return True



