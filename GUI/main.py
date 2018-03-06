from collections import OrderedDict

import os.path
import openpyxl
import encrypt as enc
import functions as func
import cgi
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from openpyxl import Workbook
import win32ui, win32gui
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import win32com.client as comclt
from bs4 import BeautifulSoup
import re
import sys
import pytz

wsh = comclt.Dispatch("WScript.Shell")

def readPath():
    f = open("chromepath.txt", "r").readlines()
    makeitastring = ''.join(map(str, f))
chromePath = readPath()

service = service.Service('chromedriver.exe')
capabilities = {'chrome.binary': chromePath}
service.start()
driver = webdriver.Remote(service.service_url, capabilities)

password = b'insecure password'

paydetails = OrderedDict([('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''), ('Addr3', ''),
                          ('City', ''), ('Post/zip code', ''), ('Country', ''), ('Cardno', ''), ('CardCVV', ''),
                          ('CardMonth', ''), ('CardYear', ''), ('CardType', '')])



def main():
  func.intro()
  enc.checkIfStore()
  func.openPage(driver)
  #asks if user wants to use stored details
  
  #if user enters 'no' will open details.html
  #asks when all details are completed if user wants to save shipping details
  #runs as normal

  #if user enters 'yes' will open details2.html
  #runs as normal after pressing enter
  #will automatically use saved shipping details




useConfig = False
  
if __name__== "__main__":
  main()

