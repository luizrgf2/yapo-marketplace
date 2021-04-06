from selenium import webdriver
import undetected_chromedriver
from loja_yapo import pesquisa
from leitor_escritor_exel import *
import numpy

def webdriver_complete(visivel:bool):

    undetected_chromedriver.install() # baixando o chromedriver indetectavel.


    option = webdriver.ChromeOptions()

    if visivel == False:
        option.add_argument('--headless')



    driver = webdriver.Chrome(executable_path='./chromedriver.exe')


    return driver

driver = webdriver_complete(True)


def main():

    file_read = leitor_exel()

    try:

        pg = int(file_read['pg'])
        pesquisa(driver, file_read['pesquisa'], pg, file_read['output_file'])
    
    except:
        
        pesquisa(driver, file_read['pesquisa'], 1, file_read['output_file'])

    driver.close()

main()