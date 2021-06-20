import mysql.connector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException  

from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq# Web client
from urllib import request as rq
import urllib 
import time
import json
import xlrd

import datetime
import pandas as pd
from pandas import read_excel
import urllib.request
import re
import csv
import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs
import os
x=datetime.datetime.now()
debug = True



#Extraccion de links de productos en categorias
link_subcategories_link = []
mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
mycursor = mydb.cursor()
sql = "SELECT * FROM sub_categories"
mycursor.execute(sql)
link_subcategories = mycursor.fetchall()
for x in link_subcategories:
  link_subcategories_link.append(x[2])


#browser = webdriver.Chrome(ChromeDriverManager().install())

def change_proxy(proxy,port):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", proxy)
    profile.set_preference("network.proxy.http_port", port)
    profile.set_preference("network.proxy.ssl", proxy)
    profile.set_preference("network.proxy.ssl_port", port)
    browser = webdriver.Firefox(profile)
    return browser



def check_exists_by_class(xpath):
    if browser.find_elements_by_css_selector(xpath):
        return True
    else:
        return False


browser = webdriver.Firefox(executable_path=r'firefox.exe')
linkssss = ['https://listado.mercadolibre.cl/case-gamer-atx#D[A:case%20gamer%20atx]']
#https://listado.mercadolibre.cl/bebes/vestuario/trajes-bano/_Desde_1501
#https://listado.mercadolibre.cl/bebes/otros/
#https://listado.mercadolibre.cl/bebes/vestuario/trajes-bano/
#https://autos.mercadolibre.cl/accesorios/gps/_Envio_Full#applied_filter_id%3Dshipping%26applied_filter_name%3DEnv%C3%ADo%26applied_filter_order%3D4%26applied_value_id%3Dfulfillment%26applied_value_name%3DFull%26applied_value_order%3D2%26applied_value_results%3D4%26is_custom%3Dfalse
nombres = []



pagination = []
urls_productos = []
nextpage = True

for i in range(len(linkssss)):
    browser.get(linkssss[i])
    #table  = browser.find_elements_by_class_name("ui-search-layout__item")
    while (nextpage):
        if browser.find_elements_by_css_selector('.andes-pagination__button--next'):
            urls =  browser.find_element_by_class_name('andes-pagination__button--next')
            print(urls.find_element_by_tag_name('a').get_attribute('href'))
            pagination.append(urls.find_element_by_tag_name('a').get_attribute('href'))
            urls = urls.find_element_by_tag_name('a')
            browser.execute_script("arguments[0].click();", urls)
            time.sleep(3)
        else:
            nextpage = False
   
#Extract link productos
for i in range(len(pagination)):
    browser.get(pagination[i])
    urlsContainer =  browser.find_element_by_class_name('ui-search-layout--stack')
    urlsContainer = urlsContainer.find_elements_by_class_name('ui-search-layout__item')
    for j in range(len(urlsContainer)):
       urls_productos.append(urlsContainer[j].find_element_by_tag_name('a').get_attribute('href'))
       print(str(j) + ' de ' + str(len(pagination)) + ' Paginaciones escaneadas')
       


# Extract info de productos
for i in range(len(urls_productos)):
    browser.get(urls_productos[i])
    time.sleep(2)
    if browser.find_elements_by_css_selector('.ui-pdp-title'):
        nombres.append(browser.find_element_by_class_name('ui-pdp-title'))
        
    else:
        nombres.append('0')
    print(str(i) + ' de ' + str(len(urls_productos)) + ' Urls de productos escaneadas')


for i in range(len(urls_productos)):
    mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
    mycursor = mydb.cursor()
    #stock = ''.join([n for n in stock[i] if n.isdigit()])
    stock = 1
    #nombre = nombre[i]
    #nombre = nombre.replace("'", "")
 
    #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
    sql = "INSERT INTO producto (nombre, stock) VALUES ('"+ str(nombres[i]) +"', '" + str(stock) + "')"
    #'"++"','"+str(x)+"','"++"','"++"','"+str(disponibles[j])+"','"++"', '"+str(description[j])+"','"+"','"++"','"+)+"
    mycursor.execute(sql)
    mydb.commit()   
print(len(nombres))