from selenium import webdriver
from time import sleep as tm
from api_conversora import dolar_real
from scraping_anuncio import req
import xlsxwriter
import os

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
        text_read = 'ID do produto[]Nome[]Link[]Loja[]Imagem[]Preço[]Vendedor[]Cidade[]Estado[]Estoque inicial[]Estoque atual[]Estoque vendido'

    text_read=text_read+'\n'+f'[]{titulo}[]{link_produto}[]Yapo[]{image_link}[]{preco}[]{nome_vendedor}[]{cidade}[]{estado[0]}[][][]'

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


                if str(titulo).upper().find(pesquisa) != -1 or str(titulo).lower().find(pesquisa) != -1 or str(titulo).title().find(pesquisa) != -1: # virificando se existe o termo da pesquisa no titulo do anuncio.

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


    
    