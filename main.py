from selenium import webdriver
import undetected_chromedriver
from loja_yapo import pesquisa

def webdriver_complete(visivel:bool):

    undetected_chromedriver.install() # baixando o chromedriver indetectavel.


    option = webdriver.ChromeOptions()

    if visivel == False:
        option.add_argument('--headless')



    driver = webdriver.Chrome(executable_path='./chromedriver.exe')


    return driver

driver = webdriver_complete(True)

pesquisa(driver, 'camisa')