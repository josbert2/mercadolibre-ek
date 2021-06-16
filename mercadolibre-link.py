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
mydb = mysql.connector.connect(
host='localhost', port=3306, user='root', passwd='', db='mercado-libre')
mycursor = mydb.cursor()
#sql = "INSERT INTO productos (id, ref, nombre,description_corta,description_larga,imagen,precio,ficha_tecnica, links, vendedora) VALUES (%s, %s)"
sql = "TRUNCATE link"
mycursor.execute(sql)
sql = "TRUNCATE sub_categories"
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

        


