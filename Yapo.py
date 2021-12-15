from selenium import webdriver
import undetected_chromedriver
import numpy
import os
from time import sleep as tm
import xlsxwriter
import pandas as pd
import requests


def dolar_real(valor_dolar:float):

    resposta = requests.get('https://www.google.com/search?q=pre%C3%A7o+dolar&sxsrf=ALeKk03jZmajJotkZ_B4B8AkzuJLVXWzTg%3A1617294963197&ei=c_ZlYJfAC6XD5OUPs6WtsA8&oq=pre%C3%A7o+dola&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQsQMyBQgAELEDMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BwgAEEcQsAM6BAgjECc6BAgAEEM6CAguELEDEIMBOgUILhCxAzoICAAQsQMQgwE6BwguELEDEEM6CQgjECcQRhD5AToKCAAQsQMQgwEQQzoHCAAQyQMQQzoHCAAQsQMQQzoPCAAQsQMQgwEQQxBGEIICUKM_WKFLYKBTaANwAngAgAHeAYgBzBGSAQUwLjMuOJgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=gws-wiz')
    
    text_init = resposta.text.split('class="BNeawe iBp4i AP7Wnd"><div><div class="BNeawe iBp4i AP7Wnd">')[1].split(' Real brasileiro</div></div>')[0]

    valor_final = float(text_init.split(',')[0]+'.'+text_init.split(',')[1])

    valor_aux = float(valor_dolar*valor_final).real

    valor_string = ''
    try:
        valor_string = str(valor_aux).split('.')[0]+','+str(valor_aux).split('.')[1]+'.'+str(valor_aux).split('.')[2]
    except:
        valor_string = str(valor_aux).split('.')[0]+','+str(valor_aux).split('.')[1]
    return valor_string

def preco_final(numero_str:str):
    
    quebrar = numero_str.split('.')
    
    preco = ''
    
    for i in range(len(quebrar)):
        
        if i != len(quebrar) - 1:
            
            preco = preco+quebrar[i]
            
        else:
            
            preco = preco+'.'+quebrar[i]
    return float(preco)

def req(link):

    response= requests.get(link,verify=True)

    text_editavel = response.text

    try:
        regiao_aux = text_editavel.split('region="')[3].split('"')[0]
    except:
        print("Erro ao pegar região.")
    
    try:
        nome_vendedor = text_editavel.split("username='")[1].split("'")[0]
    except:
        print("Erro ao pegar nome vendedor.")
    
    try:
        estado = regiao_aux.split(',')[0]
    except:
        print("Erro ao pegar estado.")

    try:
        cidade = regiao_aux.split(',')[1]
    except:
        print("Erro ao pegar cidade.")

    try:
        nome_anuncio = text_editavel.split("'Title': '")[1].split("'")[0]
    except:
        print("Erro ao pegar nome do anuncio.")

    try:
        id_anuncio = text_editavel.split("'Ad ID': ")[1].split(',')[0]
    except:
        print("Erro ao pegar o id do anuncio.")

    try:
        preco = 'R$ '+dolar_real(preco_final(text_editavel.split('data-price="$ ')[1].split('"')[0]))
    except:
        print("Erro ao pegar o preço do produto.")

    image_link = ""
    try:
        image_link = 'https://img.yapo.cl/images'+text_editavel.split('<img src="https://img.yapo.cl/images')[1].split('" ')[0]
    except:
        print("Erro ao pegar o link da imagem.")
    
    

    return {


        'nome_vendedor':nome_vendedor,
        'estado':estado,
        'cidade':cidade,
        'nome_anuncio':nome_anuncio,
        'id_anuncio':id_anuncio,
        'preco':preco,
        'image_link':image_link
    }

def salvar_no_doc(outputfile):


    tm(1)
    try:
        file_read = open('tmp.csv', 'r', encoding='utf8').read().split('\n')
    except:
        print('Não possui arquivo temporario!')
        return
    workbook = xlsxwriter.Workbook(outputfile)

    worksheet = workbook.add_worksheet()

    for i in range(len(file_read)):



        linha_atual = file_read[i].split('[]')
        

        worksheet.write(f'A{i+1}', linha_atual[0])
        worksheet.write(f'B{i+1}', linha_atual[1])
        worksheet.write(f'C{i+1}', linha_atual[2])
        worksheet.write(f'D{i+1}', linha_atual[3])
        worksheet.write(f'E{i+1}', linha_atual[4])
        worksheet.write(f'F{i+1}', linha_atual[5])
        worksheet.write(f'G{i+1}', linha_atual[6])
        worksheet.write(f'H{i+1}', linha_atual[7])
        worksheet.write(f'I{i+1}', linha_atual[8])
        worksheet.write(f'J{i+1}', linha_atual[9])
        worksheet.write(f'K{i+1}', linha_atual[10])
        worksheet.write(f'L{i+1}', linha_atual[11])
        worksheet.write(f'M{i+1}', linha_atual[12])

    workbook.close()

    try:
        os.remove('tmp.csv')
    except:
        print('Finalizado')

def salvar_dados_xml_saida(produto):

        
        
    
    id_produto = produto['id']
    image_link = produto['image_link']
    preco = produto['preco']
    link_produto = produto['link_produto']
    titulo = produto['titulo']
    cidade = produto['cidade']
    estado = produto['estado'],
    nome_vendedor = produto['nome_vendedor']


    text_read = ''


    try:
        text_read = open('tmp.csv','r',encoding='utf8').read()
    except:
        text_read = 'ID do produto[]Nome[]Link[]Loja[]Imagem[]Preço[]Vendedor[]Cidade[]Estado[]Estoque inicial[]Estoque atual[]Estoque vendido[]Código do produto'

    text_read=text_read+'\n'+f'[]{titulo}[]{link_produto}[]Yapo[]{image_link}[]{preco}[]{nome_vendedor}[]{cidade}[]{estado[0]}[][][][]{id_produto}'

    open('tmp.csv','w',encoding='utf8').write(text_read)

def pegando_dados(driver:webdriver,pesquisa:str,page_start:int,output_file):


    '''Irá entrar no site e navegara entre paginas verificando se o anuncio possui as caracteristicas desejadas.'''


    pesquisa_final = pesquisa.replace(' ', '+') #modificando a string de pesquisa para url final

    produtos_final = [] #lista para ir adicionando

    url_base = f'https://www.yapo.cl/chile?ca=15_s&q={pesquisa_final}&o=' # url base

    i = page_start # numero interavel

    while True: # irá navegar entre as páginas e irá pegar todas as informaçoes

        driver.get(url_base+str(i))

        while True: #esperando o carregamento do site

            try:
                driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div')
                break

            except Exception as e:
                print(e)
        
        
        
        tm(4)
        
        
        produtos = driver.execute_script('var a = document.getElementsByClassName("ad listing_thumbs"); return a') #pegando os produtos

        if len(produtos) == 0: # caso venha uma lista vazia de produtos será parada a execução

            break


        for produto in produtos:

            link_produto = produto.find_element_by_class_name('title').get_attribute('href')

            try:
               
                Req = req(link_produto)


                titulo = Req['nome_anuncio']


                if str(titulo).lower().find(pesquisa.lower()) != -1: # virificando se existe o termo da pesquisa no titulo do anuncio.

                    print('Contem o termo ||'+titulo)



            
                    produto_final ={
                        'id':Req['id_anuncio'],
                        'image_link':Req['image_link'],
                        'preco':Req['preco'],
                        'link_produto':link_produto,
                        'titulo':titulo,
                        'cidade':Req['cidade'],
                        'estado':Req['estado'],
                        'nome_vendedor':Req['nome_vendedor']
                    }

                    salvar_dados_xml_saida(produto_final)
            except Exception as e:
                print(e)
                pass

        i+=1





    
    return produtos_final

def pesquisa(driver:webdriver,pesquisa:str,page_start:int,output_file):

    produtos = pegando_dados(driver,pesquisa,page_start,output_file)
    salvar_no_doc(output_file)

def leitor_exel():

    excel_entrada = pd.read_excel('robo_mktplace.xlsx',0 )

    temo_pesquisa = excel_entrada['NOME_SITE'][0]
    id_produto = excel_entrada['ID_PRODUTO'][0]
    id_marca = excel_entrada['ID_MARCA'][0]
    PG = excel_entrada['PG'][0]
    output_file = excel_entrada['OUTPUT_FILE'][0]


    return {'pesquisa':temo_pesquisa, 'if_produto':id_produto, 'id_marca':id_marca, 'pg':PG, 'output_file':output_file}

def webdriver_complete(visivel:bool):

    undetected_chromedriver.install() # baixando o chromedriver indetectavel.


    option = webdriver.ChromeOptions()

    if visivel == False:
        option.add_argument('--headless')




    driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)


    return driver

driver = webdriver_complete(True)

def main():

    file_read = leitor_exel()

    try:

        pg = int(file_read['pg'])
        pesquisa(driver, str(file_read['pesquisa']).lower(), pg, file_read['output_file'])
    
    except:
        
        pesquisa(driver, str(file_read['pesquisa']).lower(), 1, file_read['output_file'])

    driver.close()


    

main()