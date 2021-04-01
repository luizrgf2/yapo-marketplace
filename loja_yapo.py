from selenium import webdriver
from time import sleep as tm

def pegando_dados(driver:webdriver,pesquisa:str):

    pesquisa_final = pesquisa.replace(' ', '+') #modificando a string de pesquisa para url final

    produtos_final = [] #lista para ir adicionando

    url_base = f'https://www.yapo.cl/chile?ca=15_s&q={pesquisa_final}&o=' # url base

    i = 1 # numero interavel

    while True:
        
        produtos = driver.execute_script('var a = document.getElementsByClassName("ad listing_thumbs"); return a') #pegando os produtos

        if len(produtos) == 0:

            break


        for produto in produtos:

            titulo = produto.find_element_by_class_name('title').text


            if str(titulo).upper().find(pesquisa) != -1 or str(titulo).lower().find(pesquisa) != -1 or str(titulo).title().find(pesquisa) != -1: # virificando se existe o termo da pesquisa no titulo do anuncio.

                print('Contem o termo ||'+titulo)

                produtos_final.append(produto)

        i+=1


        driver.get(url_base+str(i))

        while True: #esperando o carregamento do site

            try:
                driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div')
                break

            except Exception as e:
                print(e)
        tm(4)
        
def pesquisa(driver:webdriver,pesquisa:str):


    driver.get('https://www.yapo.cl/chile')

    while True: #esperando o carregamento do site
        try:
            
            driver.find_element_by_xpath('/html/body/div[1]/div[5]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[1]/div/ul/li[1]')
            break

        except Exception as e:
            print(e)

    #pesquisando pelo termo

    driver.find_element_by_name('q').send_keys(pesquisa)

    
    #apertando botão de pesquisa

    driver.find_element_by_id('searchbutton').click()

    while True: #esperando o carregamento do site
        try:
            
            driver.find_element_by_xpath('/html/body/div[1]/div[5]/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td[1]/div/ul/li[1]')
            break

        except Exception as e:
            print(e)

    

    pegando_dados(driver,pesquisa)


    
    