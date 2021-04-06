from selenium import webdriver
from time import sleep as tm
from api_conversora import dolar_real
import pandas as pd

def salvar_dados_xml_saida(output_file_name:str,produto):

        
        
    
    id_produto = produto['id']
    image_link = produto['image_link']
    preco = produto['preco']
    link_produto = produto['link_produto']
    titulo = produto['titulo']
    cidade = produto['cidade']
    estado = produto['estado']


    text_read = ''


    try:
        text_read = open('tmp.csv','r',encoding='utf8').read()
    except:
        text_read = 'ID do produto,Nome,Link,Loja,Imagem,Preço,Vendedor,Cidade,Estado,Estoque inicial,Estoque atual,Estoque vendido'

    text_read=text_read+'\n'+f'{id_produto},{titulo},{link_produto},Yapo,{image_link},{preco},,{cidade},{estado},,,'

    open('tmp.csv','w',encoding='utf8').write(text_read)

    file_csv = pd.read_csv('tmp.csv')
    file_csv.to_excel(output_file_name)






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

            titulo = produto.find_element_by_class_name('title').text


            if str(titulo).upper().find(pesquisa) != -1 or str(titulo).lower().find(pesquisa) != -1 or str(titulo).title().find(pesquisa) != -1: # virificando se existe o termo da pesquisa no titulo do anuncio.

                print('Contem o termo ||'+titulo)



                try:
                    preco_parcial = float(produto.find_element_by_class_name('price').text.strip(' ').split('$ ')[1])
                    preco = dolar_real(preco_parcial)

                
                
                    id_produto = produto.get_attribute('id')
                    image_link = produto.find_element_by_class_name('image').get_attribute('src')
                    link_produto = produto.find_element_by_class_name('title').get_attribute('href')
                    titulo = produto.find_element_by_class_name('title').text
                    cidade = produto.find_element_by_class_name('commune').text
                    estado = produto.find_element_by_class_name('region').text

                    
                    produto_final ={
                        'id':id_produto,
                        'image_link':image_link,
                        'preco':preco,
                        'link_produto':link_produto,
                        'titulo':titulo,
                        'cidade':cidade,
                        'estado':estado
                    }

                    salvar_dados_xml_saida(output_file, produto_final)
                except Exception as e:
                    print(e)

        i+=1





    
    return produtos_final


def pesquisa(driver:webdriver,pesquisa:str,page_start:int,output_file):

    produtos = pegando_dados(driver,pesquisa,page_start,output_file)



    
    