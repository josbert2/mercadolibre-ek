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


links = ['https://articulo.mercadolibre.cl/MLC-584794512-convertidor-de-hdmi-para-vga-con-audio-philco-hd525-mirage-_JM#reco_item_pos=3&reco_backend=machinalis-pads&reco_backend_type=low_level&reco_client=vip-pads-right&reco_id=784415c6-ae50-4638-9728-5486e5ec72f6&is_advertising=true&ad_domain=VIPCORE_RIGHT&ad_position=4&ad_click_id=M2MxNmQwMjMtNjQxMC00OTgwLTk0NzMtNWM3YmRjYjYyNzMx','https://articulo.mercadolibre.cl/MLC-502007700-adaptador-conversor-hdmi-a-vga-y-audio-nuevo-_JM?variation=55679244142#reco_item_pos=2&reco_backend=machinalis-seller-items&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=9432a5fe-3925-484d-ab99-46a7778b78d8','https://articulo.mercadolibre.cl/MLC-521013244-adaptador-display-port-macho-a-hdmi-hembra-nuevo-_JM#reco_item_pos=3&reco_backend=machinalis-homes&reco_backend_type=function&reco_client=home_navigation-recommendations&reco_id=6b229826-19c7-4b2d-82bb-68249242c1c3&c_id=/home/navigation-recommendations/element&c_element_order=4&c_uid=ae013512-4b4f-43e6-bd9b-6ec6759b55fd']
nombres = []
stock = []
for i in range(len(links)):
    
  
  
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


