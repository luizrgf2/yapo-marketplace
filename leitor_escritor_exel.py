import pandas as pd


def leitor_exel():

    excel_entrada = pd.read_excel('robo_mktplace.xlsx',0 )

    temo_pesquisa = excel_entrada['NOME_SITE'][0]
    id_produto = excel_entrada['ID_PRODUTO'][0]
    id_marca = excel_entrada['ID_MARCA'][0]
    PG = excel_entrada['PG'][0]
    output_file = excel_entrada['OUTPUT_FILE'][0]


    return {'pesquisa':temo_pesquisa, 'if_produto':id_produto, 'id_marca':id_marca, 'pg':PG, 'output_file':output_file}