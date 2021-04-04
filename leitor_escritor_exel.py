import pandas as pd


def leitor_exel():

    excel_entrada = pd.read_excel('./robo_mktplace.xlsx',sheet_name=None)

    print(excel_entrada['NOME_SITE'][0])

leitor_exel()