from selenium import webdriver
from time import sleep as tm

def pegando_dados(driver:webdriver,pesquisa:str):



    produtos_final = [] #lista para ir adicionando

    url_base = f'https://www.yapo.cl/chile?ca=15_s&q={pesquisa}&o=' # url base

    i = 1 # numero interavel

    while True:
        
        produtos = driver.execute_script('var a = document.getElementsByClassName("ad listing_thumbs"); return a') #pegando os produtos

        print(len(produtos))

        for produto in produtos:

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

    pesquisa_final = pesquisa.replace(' ', '+')

    pegando_dados(driver,pesquisa_final)


    
    