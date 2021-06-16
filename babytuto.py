from openpyxl import Workbook

import mysql.connector
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException  

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

import requests
from urllib import request as rq

#import psycopg2
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq# Web client

import urllib 
import time
import json
import xlrd
#import master_functions as mf
import datetime
import pandas as pd
from pandas import read_excel

import time
import os

workbook = xlrd.open_workbook("products.xml.xlsx","rb")
sheets = workbook.sheet_names()
links = []
for sheet_name in sheets:
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows):
        row_valaues = sh.row_values(rownum)
        links.append(row_valaues[3])
 

nombres=[]
marca=[]
precioOriginal=[]
precioOferta=[]
stock=[]
sku=[]
bestseller=[]
description=[]
imagenes_list=[]
linksbd=[]
description_corta=[]
description_larga=[]
linkstobd = []


category_list = []

for i in range(len(links)):
    
    if i < 5000:
        linkstobd.append(links[i])
        linksbd.append(str(links[i]))
        print('Link: ' + str(i) + '------------------------------------------------------')
        #link_f.append(llinks[i])
        try:
            req = rq.Request(links[i], headers={'User-Agent': 'Mozilla/5.0'})
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


        
            #Nombre
        news_panel = page_soup.select('.title-right .title')[0]
        if len(news_panel)==0:
            nombres.append('Algo pasa')
        else:
            temp = news_panel.text
            if temp:
                #print(str(temp.text))
                nombres.append(str(temp))

        news_panel = page_soup.select('.merchant-name')[0]
        if len(news_panel)==0:
            nombres.append('Algo pasa')
        else:
            temp = news_panel.text
            if temp:
                #print(str(temp.text))
                marca.append(str(temp))
            


        
            
        if len(page_soup.find(class_='price').find(class_='original').contents) > 0:
            table = page_soup.find(class_='price').find(class_='original')

            precioOriginal.append(table.text)
        else:
            precioOriginal.append('No existe')

        

        table = page_soup.find(class_='price').find(class_='final')
        if table:
            table = page_soup.find(class_='price').find(class_='final')

            precioOferta.append(table.text)
        else:
            precioOferta.append('No existe')

        news_panel = page_soup.select('.stock-remaining')
    
        if len(news_panel)>0:
            stock.append(news_panel[0]['data-stock'])
        else:
            #print(str(temp.text))
            stock.append("Existe")

        
        

        table = page_soup.find("div", {"id": "description"}).find(class_='details')
        if  table:
            de = str(table)
            description.append(str(de[:1000000]))
            #b_arr = '\n'.join([x.text for x in table])
            #description.append(b_arr.encode('utf-8'))
        else:
            description.append('No tiene')


        table2 = page_soup.find("div", {"id": "data-sheet"})
        if table2.find("tbody") == None:
            description_corta.append('No tiene')
        else:
            if  len(table2.find("tbody")) > 0:
                
                de = str(table)
                description_corta.append(str(de[:1000000]))
                #b_arr = '\n'.join([x.text for x in table])
                #description.append(b_arr.encode('utf-8'))
            else:
                description_corta.append('No tiene')



        categorys = page_soup.find('ul', attrs={'class': 'breadcrumb'})
    
        main_category = ''
        for div in categorys.findAll('li'):
            main_category += div.text.replace("»", "-")
        category_list.append( main_category)


        images_box = page_soup.find('div', attrs={'id': 'product-pictures'})
        imagenes = ""
        
        for div in images_box.findAll('img'):
            imagenes += div['src'] + ","
            if div == images_box.findAll('img')[-1]:
                imagenes += div['src']


        imagenes_list.append(imagenes)
    


    

        images_box = page_soup.findAll('img', {'class': 'tag'})
    
        if len(images_box) > 0:
            
            for div in images_box:
            
                if div['src'] == 'https://s3.babytuto.com/img/BEST_SELLER.png':
                    bestseller.append('1')
                    print("Es seller")
                
                    
        else:
            print("No Es seller")
            bestseller.append('0') 
    
            
        
        """if images_box is None :
            print('no tiene')
        else:
            for div in images_box.findAll('img'):
                print(div['src']) """  
        
        
        """if len(news_panel)==0:
            bestseller.append('Algo pasa')
        else:
            temp = news_panel.text
            if temp:
                #print(str(temp.text))
                bestseller.append(str(temp))"""
            











        
        
        """  
        table = page_soup.find(class_='attribute').find(class_='value')
        if table:
            table = page_soup.find(class_='attribute').find(class_='value')

            sku.append(table.text)
        else:
            sku.append('No existe')
    
        s = ''
        table = page_soup.find(class_='description').find(class_='value').find_all("li")
        if  table:
            b_arr = '\n'.join([x.text for x in table])
            
        
            description.append(b_arr.encode('utf-8'))
        else:
            description.append('No tiene')


        
        
        imagenes.append('NULL')
        containers = page_soup.findAll("div", {"id": "horizontal-thumbnail"})
        
        browser = webdriver.Firefox(executable_path = './geckodriver')
        browser.get(linkst[i])
        #nav = browser.find_element_by_id("mainnav")
        time.sleep(5)
        feature_icon = browser.find_element_by_class_name("item-thumb")
        c = browser.find_element_by_id("horizontal-thumbnail")
        #parentElement = c.find_element_by_class_name("img-responsive")

        
        for img in c.find_elements_by_class_name('img-responsive'):
            img = img.get_attribute("src")
            print(str(img))

        


        images = soup.find('div', id="owl-carousel-gallery").find(class_='owl-item').find(class_='zoomImg').findAll('img')
        for image in images:
            #print image source
            print image['src']
            #print alternate text
            print image['alt']
        
        print(i)
        print(len(marca))
        print(len(nombres))
        print(len(precioOriginal))
        print(len(precioOferta))
        print(len(stock))
        print(len(imagenes))
        print(len(sku))
        print(len(linksbd))
        print(len(description))
        """
        #mydb = mysql.connector.connect(
        #host='localhost', port=3307, user='root', passwd='', db='bebesit')
        #mycursor = mydb.cursor()
        #sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
        #data = (str(nombres[i]), str(marca[i]), str(precioOriginal[i]), precioOferta[i], stock[i], sku[i],  description[i], linksbd[i])
        #sql = ("INSERT INTO productos (nombre, marca, precioNormal, precioOferta, stock, sku,  detalles, link)"
        #    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        #mycursor.execute(sql, data)
        #mydb.commit()
"""print(nombres)    
print(marca)   
print(stock)
print(precioOriginal)
print(precioOferta)
#print(category_list)
print(imagenes_list)
print(str(str(imagenes_list[0])))
"""


print(len(nombres))
print(len(stock))
print(len(marca))
print(len(precioOriginal))
print(len(precioOferta))
print(len(imagenes_list))
print(len(bestseller))
print(len(description_corta))
print(len(description))
print(len(category_list))
print(len(linkstobd))
print(len(bestseller))
for w in range(len(linkstobd)):
    print('datos a ingresar: -----------')
   
    #print(description[w])
    print('-----------')
    mydb = mysql.connector.connect(
    host='localhost', port=3306, user='root', passwd='', db='babytuto')
    mycursor = mydb.cursor()
    sql = "INSERT INTO productos (nombre, categorias, marca, stock, precio_original, precio_oferta, imagenes, description_larga, description_corta, bestseller, links) VALUES ('" + str(nombres[w]) + "', '" + str(category_list[w]) + "', '" + str(marca[w]) + "', '" + str(stock[w]) + "', '" + str(precioOriginal[w]) + "', '" + str(precioOferta[w]) + "', '" + str(str(imagenes_list[w])) + "', '" + str(str(description[w])) + "', '" + str(str(description_corta[w])) + "', '" + str(bestseller[w]) + "', '" + str(linksbd[w]) + "')" 
    mycursor.execute(sql)
    mydb.commit()