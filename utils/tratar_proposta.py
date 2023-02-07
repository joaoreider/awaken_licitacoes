
def tratar_proposta_excel_md(path_da_proposta):
    print('Lendo proposta...')
    proposta_ok = 0
    try:
        from pandas import read_excel
        proposta = read_excel(path_da_proposta)
        print('Proposta lida!')
        proposta_ok = 1
    except:
        print('Erro ao ler propostar.')
        proposta_ok = 0

    print('Extraindo colunas Item, Descrição, Marca e Preço Unitário')
    try:

        dict_resultado = {}
        proposta_item = []
        proposta_descricao_do_item = []
        proposta_marca = []
        proposta_preco_unitario = []

        
        for i in range(len(proposta)):

            indice = proposta.iloc[i].values[[2,5, 15, 21]]
           
            print(indice)
            if '< Registro ANVISA : ' in str(indice[1]):
                proposta_item.append(indice[0])
                proposta_descricao_do_item.append(indice[1])
                proposta_marca.append(indice[2])
                proposta_preco_unitario.append(indice[3])
               


        dict_resultado['Item'] =  proposta_item
        dict_resultado['Descrição do Item'] = proposta_descricao_do_item
        dict_resultado['Marca'] = proposta_marca
        dict_resultado['Preço Unitário'] = proposta_preco_unitario

        descricao = proposta_descricao_do_item
        from pandas import DataFrame
        proposta = DataFrame(dict_resultado)
        print('Ok!')
        proposta_ok = 1

    except:
        print('Erro ao extrair colunas.')
        proposta_ok = 0

    print('Extraindo o registro da descrição...')
    try:

        # Extrai só o registro da planilha de descrição do item
        temp = proposta['Descrição do Item'].apply(
            lambda x: str(x).split('Registro ANVISA :')[1])

        temp2 = list(temp.apply(lambda x: str(x).split('>')[0]))

        proposta['Registros'] = list([int(x.strip()) for x in temp2])
        print()
        print(proposta['Registros'])
        print()

        proposta_ok = 1
        print('Ok')

    except:
        print('Erro ao extrair registro.')
        proposta_ok = 0

    return proposta_ok, proposta, descricao

