import mysql.connector
from selenium import webdriver
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
if debug:
    mydb = mysql.connector.connect(
    host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
    mycursor = mydb.cursor()
    #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
    sql = "TRUNCATE link"
    mycursor.execute(sql)
    sql = "TRUNCATE sub_categories"
    mycursor.execute(sql)
    sql = "TRUNCATE producto"
    mycursor.execute(sql)
    mydb.commit()

urls =  'https://www.mercadolibre.cl/c/bebes#c_id=/home/categories/category-l1/category-l1&c_category_id=MLC1384&c_uid=93c464f6-ce96-11eb-96dc-27f8d1cb6fe6'
links_producto=[]
sub_categories = []
sub_categories_link = []
ids=[]


req = rq.Request(urls, headers={'User-Agent': 'Mozilla/5.0'})
webpage = uReq(req).read()
uClient = uReq(req)
page_soup = soup(uClient.read(), "html.parser" )
uClient.close()
productDivs = page_soup.findAll("div", {"class": "desktop__view-child"})
i = 0
ii = 0
for div in productDivs:
    #links_producto.append(str(div.find('a')['href']))
    links_producto = str(div.find('a')['href'])
    subCategories =  div.find('a')
    li = div.findAll("li", {"class": "category-list__item"})
    mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
    mycursor = mydb.cursor()
    #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
    sql = "INSERT INTO link (nombre, id_categoria) VALUES ('"+ str(links_producto) +"', '"+ str(i) +"')"
    #'"++"','"+str(x)+"','"++"','"++"','"+str(disponibles[j])+"','"++"', '"+str(description[j])+"','"+"','"++"','"+)+"
    mycursor.execute(sql)
    mydb.commit()
    i += 1
    for divs in li:
        sub_categories = divs.find('a').text.strip()
       
        sub_categories_link = str(divs.find('a')['href'])
      
        mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
        mycursor = mydb.cursor()
        #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
        sql = "INSERT INTO sub_categories (nombre, link_sub, id_cat) VALUES ('"+ str(sub_categories) +"', '"+ str(sub_categories_link) +"', '" + str(i) + "')"
        #'"++"','"+str(x)+"','"++"','"++"','"+str(disponibles[j])+"','"++"', '"+str(description[j])+"','"+"','"++"','"+)+"
        mycursor.execute(sql)
        mydb.commit()
        ii += 1


#Extraccion de links de productos en categorias
link_subcategories_link = []
mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
mycursor = mydb.cursor()
sql = "SELECT * FROM sub_categories"
mycursor.execute(sql)
link_subcategories = mycursor.fetchall()
for x in link_subcategories:
  link_subcategories_link.append(x[2])




linkTEST = ['https://listado.mercadolibre.cl/bebes/vestuario/trajes-bano/#CATEGORY_ID=MLC418805&S=hc_bebes']
#https://listado.mercadolibre.cl/bebes/vestuario/trajes-bano/_Desde_1501
## Extract links by categories
pagination = False
new_link = ''
for i in range(len(linkTEST)):
    print('Link: ' + str(i) + '------------------------------------------------------')
    #link_f.append(llinks[i])
    try:
        req = rq.Request(linkTEST[i], headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('s')

    try:
        webpage = uReq(req).read()
    except rq.HTTPError: #Si se cae la internet que no se caiga el programa
        continue
    except UnicodeEncodeError: #Si el link esta raro, que lo omita
        nombres.append('Revisar Nombre')
    
        continue
    except urllib.error.URLError: #Si el link no existe que lo omita

        nombres.append('Revisar Nombre')
      #link_test.append(link_test[i])
    uClient = uReq(req)
    try:
        page_soup = soup(uClient.read(), "html.parser")
    except rq.IncompleteRead: #Si no puede leer que lo omita
        nombres.append('404')
        continue
    uClient.close()

    productDivs = page_soup.findAll("li", {"class": "ui-search-layout__item"})
    for div in productDivs:
        print(div.find('a')['href'])

    productDivs = page_soup.findAll("li", {"class": "andes-pagination__button--next"})
    if len(productDivs)==0:
        pagination = False
    else:
        pagination = True
        for div in productDivs:
            new_link = div.find('a')['href']
   
    quit()



# Extraccion de datos de cada producto
links = [link_subcategories_link]
nombres = []
stock = []
for i in range(len(link_subcategories_link)):
    print('Link: ' + str(i) + '------------------------------------------------------')
    #link_f.append(llinks[i])
    try:
        req = rq.Request(link_subcategories_link[i], headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print('s')

    try:
        webpage = uReq(req).read()
    except rq.HTTPError: #Si se cae la internet que no se caiga el programa
        continue
    except UnicodeEncodeError: #Si el link esta raro, que lo omita
        nombres.append('Revisar Nombre')
    
        continue
    except urllib.error.URLError: #Si el link no existe que lo omita

        nombres.append('Revisar Nombre')


        
    #link_test.append(link_test[i])
    uClient = uReq(req)
    try:
        page_soup = soup(uClient.read(), "html.parser")
    except rq.IncompleteRead: #Si no puede leer que lo omita
        nombres.append('404')
        continue
    uClient.close()


    news_panel = page_soup.select('.ui-pdp-media__title-icons')
    
    if len(news_panel)==0:
        print('f')
    else:
        print("Tag Found")


    news_panel = page_soup.select('.ui-pdp-buybox__quantity__available')

    if len(news_panel)>0:
        stock.append(news_panel[0].text)
    else:
        #print(str(temp.text))
        stock.append("Existe")


    news_panel = page_soup.select('.ui-pdp-title')[0]
    if len(news_panel)==0:
        nombres.append('Algo pasa')
    else:
        temp = news_panel.text
        if temp:
            #print(str(temp.text))
            nombres.append(str(temp))

        
print(nombres)
print(stock)

for i in range(len(link_subcategories_link)):
    mydb = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
    mycursor = mydb.cursor()
    stock = ''.join([n for n in stock[i] if n.isdigit()])
    nombre = nombres[i]
    nombre = nombre.replace("'", "")
 
    #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
    sql = "INSERT INTO producto (nombre, stock) VALUES ('"+ str(nombre) +"', '" + str(stock) + "')"
    #'"++"','"+str(x)+"','"++"','"++"','"+str(disponibles[j])+"','"++"', '"+str(description[j])+"','"+"','"++"','"+)+"
    mycursor.execute(sql)
    mydb.commit()    
 


#Menu mobile un poco mas ancho
##Esta fijo boton de limpia y curvo ---
##X de cerrar como div completo 
##6 imagenes en agregar producto##
##iphone 5 acomodar diseño
#Filtros mobile
#Ordenar acomodar en mobile
#imagene del producto con     object-fit: contain;
##Padding de mensaje en modal de producto
#Buscador en 1776 mas grande
##Curvo filtro de limpiar 
##y paginacion con mockup
#Revisar form de mensaje enviado
##Revisar botones de compartir
##Boton de facebook en mobile