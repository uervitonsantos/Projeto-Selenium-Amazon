# Codigo para extração de dados do site da Amazon#

from urllib.error import URLError, HTTPError
from lxml import html
from bs4 import BeautifulSoup
import time
import pandas as pd
import xlsxwriter
import requests
from selenium import webdriver

# Variavel que recebe o item a ser consultado
textsearch = ("Iphone")


# classe principal
class AmazonBot:
    def __init__(self):
        try:
            # Inicia o webdrive do Google Chrome
            self.browser = webdriver.Chrome(
                executable_path=r'C:\selenium browser driver\chromedriver_win32\chromedriver.exe')
            # Pegar conteúdo HTML a partir da URL
            self.browser.get("https://www.amazon.com.br/")
            # Exceções para validar a conexão com a pagina
        except HTTPError as e:
            print(e)
        except URLError:
            print("Servidor fora do ar ou Dominio Incorreto")
        else:
            # Insere o item no campo de busca da pagina
            self.browser.find_element_by_xpath("//input[@id='twotabsearchtextbox']").send_keys(textsearch)
            time.sleep(10)
            # Clica no botão de buscar
            self.browser.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input').click()
            time.sleep(1)

            # Metodo para Parsear o conteúdo HTML
            self.soup = BeautifulSoup(self.browser.page_source, 'lxml')

            self.myTitle = []
            self.myPrice = []

            # variavel que recebe a consulta das cláusulas h2 e span do HTML
            title = self.soup.find_all('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})
            price = self.soup.find_all('span', {'class': 'a-offscreen'})

            # loop para pegar todos os titulos e preços
            for t, p in zip(title, price):
                self.myTitle.append(t.text)
                self.myPrice.append(p.text)

    def insert_Excel(self):
        """Função cria uma tabela utilizando o framework Padas
        e e persites os dados no Excel chamado: WebScraping.xlsx """
        web = pd.DataFrame({"titulo": self.myTitle, "Preço": self.myPrice})
        print(web)
        writer = pd.ExcelWriter('WebScraping.xlsx', engine='xlsxwriter')
        web.to_excel(writer, sheet_name='Sheet1')

        writer.save()


site = AmazonBot()
site.insert_Excel()
