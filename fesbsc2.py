from configparser import ConfigParser
from collections import OrderedDict
from hashlib import sha256
import aes
from base64 import b64encode, b64decode
import time
import os.path
import openpyxl
import input_manual
import cgi
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from openpyxl import Workbook
import win32ui, win32gui
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import win32com.client as comclt
from bs4 import BeautifulSoup
import datetime
import re
import sys
from datetime import datetime
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

keywords = []

password = b'insecure password'

paydetails = OrderedDict([('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''), ('Addr3', ''),
                          ('City', ''), ('Post/zip code', ''), ('Country', ''), ('Cardno', ''), ('CardCVV', ''),
                          ('CardMonth', ''), ('CardYear', ''), ('CardType', '')])


def selectKeywords():
    keywordsInput = input("Select keywords, use a comma to separate tags and don't use any spaces e.g. Reflective,Sleeve,Logo,Puffer \n")
    split = keywordsInput.strip().split(",")
    for splits in split:
        keywords.append(splits)

sizeC = 0


checkedListings = []
def check_exists_by_xpath_no_wait(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False

def check_exists_by_xpath(xpath, driver):
    try:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)

def returnTime(hour):
    dropTime = int(hour)
    text = "Drop selected for "
    text += hour
    text += ":00"
    text += " the program will automatically run at this time. Please do not close the web browser or cmd box."
    print(text)
    while True:
        ts = time.time()
        houra = datetime.fromtimestamp(ts).strftime('%H')
        hour = int(houra)
        if hour >= dropTime:
            break
isPayPal = 0
def readDetails():
    global password
    print("Page loaded! Do you want to safe your credentials encrypted for later use? (yes/no) ")
    ready = input()
    if ready.upper() == "YES" or ready.upper() == "Y":
        safeConf = True
    else:
        safeConf = False

    name = driver.find_elements_by_xpath("""//*[@id="name"]""")
    sname = name[0].text
    if len(name) > 1:
        sname = (name[len(name) - 1].text)

    email = driver.find_elements_by_xpath("""//*[@id="order_email"]""")
    semail = email[0].text
    if len(email) > 1:
        semail = (email[len(email) - 1].text)

    tel = driver.find_elements_by_xpath("""//*[@id="order_tel"]""")
    stel = tel[0].text
    if len(tel) > 1:
        stel = (tel[len(tel) - 1].text)

    add1 = driver.find_elements_by_xpath("""//*[@id="bo"]""")
    sadd1 = add1[0].text
    if len(add1) > 1:
        sadd1 = (add1[len(add1) - 1].text)

    sadd2 = ""
    if check_exists_by_xpath_no_wait("""//*[@id="oba3"]""") == True:
        add2 = driver.find_elements_by_xpath("""//*[@id="oba3"]""")
        sadd2 = add2[0].text
        if len(add2) > 1:
            sadd2 = (add2[len(add2) - 1].text)

    sadd3 = ""
    if check_exists_by_xpath_no_wait("""//*[@id="order_billing_address_3"]""") == True:
        add3 = driver.find_elements_by_xpath("""//*[@id="order_billing_address_3"]""")
        sadd3 = add3[0].text
        if len(add3) > 1:
            sadd3 = (add3[len(add3) - 1].text)

    city = driver.find_elements_by_xpath("""//*[@id="order_billing_city"]""")
    scity = city[0].text
    if len(city) > 1:
        scity = (city[len(city) - 1].text)

    postcode = driver.find_elements_by_xpath("""//*[@id="order_billing_zip"]""")
    spostcode = postcode[0].text
    if len(postcode) > 1:
        spostcode = (postcode[len(postcode) - 1].text)

    country = driver.find_elements_by_xpath("""//*[@id="order_billing_country"]""")
    scountry = country[0].text
    if len(country) > 1:
        scountry = (country[len(country) - 1].text)

    card = driver.find_elements_by_xpath("""//*[@id="credit_card_type"]""")
    scard = card[0].text
    if len(card) > 1:
        scard = (card[len(card) - 1].text)
    if scard == "American":
        scard = "American Express"
    if scard == "PayPal":
        isPayPal = 1

    cardno = driver.find_elements_by_xpath("""//*[@id="cnb"]""")
    scardno = cardno[0].text
    if len(cardno) > 1:
        scardno = (cardno[len(cardno) - 1].text)

    month = driver.find_elements_by_xpath("""//*[@id="credit_card_month"]""")
    smonth = month[0].text
    if len(month) > 1:
        smonth = (month[len(month) - 1].text)

    year = driver.find_elements_by_xpath("""//*[@id="credit_card_year"]""")
    syear = year[0].text
    if len(year) > 1:
        syear = (year[len(year) - 1].text)

    drop = driver.find_elements_by_xpath("""//*[@id="drop_time"]""")
    sdrop = drop[0].text
    if len(drop) > 1:
        sdrop = (drop[len(drop) - 1].text)

    catType = driver.find_elements_by_xpath("""//*[@id="category_type"]""")
    scatType = catType[0].text
    if len(catType) > 1:
        scatType = (catType[len(catType) - 1].text)

    colour = driver.find_elements_by_xpath("""//*[@id="colour"]""")
    scolour = colour[0].text
    if len(colour) > 1:
        scolour = (colour[len(colour) - 1].text)

    keywords = driver.find_elements_by_xpath("""//*[@id="order_keywords"]""")
    skeywords = keywords[0].text
    print(skeywords)
    if len(keywords) > 1:
        skeywords = (keywords[len(keywords) - 1].text)

    size = driver.find_elements_by_xpath("""//*[@id="size"]""")
    ssize = size[0].text
    if len(size) > 1:
       ssize = (size[len(size) - 1].text)

    cvv = driver.find_elements_by_xpath("""//*[@id="vval"]""")
    scvv = cvv[0].text
    if len(cvv) > 1:
        scvv = (cvv[len(cvv) - 1].text)

    if safeConf:
        inp = input("\nEnter a password to continue")
        password = inp.encode('ascii')
        writeToConf('Name', sname)
        writeToConf('Email', semail)
        writeToConf('Phone', stel)
        writeToConf('Addr1', sadd1)
        writeToConf('Addr2', sadd2)
        writeToConf('Addr3', sadd3)
        writeToConf('City', scity)
        writeToConf('Post/zip Code', spostcode)
        writeToConf('Country', scountry)
        writeToConf('Cardno', scardno)
        writeToConf('CardCVV', scvv)
        writeToConf('CardMonth', smonth)
        writeToConf('CardYear', syear)
        writeToConf('CardType', scard)

        purchaseItem(sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv)

def readProduct():
    global password
    input("Page loaded! Press enter to continue")

    drop = driver.find_elements_by_xpath("""//*[@id="drop_time"]""")
    sdrop = drop[0].text
    if len(drop) > 1:
        sdrop = (drop[len(drop) - 1].text)

    catType = driver.find_elements_by_xpath("""//*[@id="category_type"]""")
    scatType = catType[0].text
    if len(catType) > 1:
        scatType = (catType[len(catType) - 1].text)

    colour = driver.find_elements_by_xpath("""//*[@id="colour"]""")
    scolour = colour[0].text
    if len(colour) > 1:
        scolour = (colour[len(colour) - 1].text)

    keywords = driver.find_elements_by_xpath("""//*[@id="order_keywords"]""")
    skeywords = keywords[0].text
    if len(keywords) > 1:
        skeywords = (keywords[len(keywords) - 1].text)

    size = driver.find_elements_by_xpath("""//*[@id="size"]""")
    ssize = size[0].text
    if len(size) > 1:
       ssize = (size[len(size) - 1].text)

    sname = readConf('Name')
    semail = readConf('Email')
    stel = readConf('Phone')
    sadd1 = readConf('Addr1')
    sadd2 = readConf('Addr2')
    sadd3 = readConf('Addr3')
    scity = readConf('City')
    spostcode = readConf('Post/zip code')
    scountry = readConf('Country')
    scard = readConf('CardType')
    scardno = readConf('Cardno')
    smonth = readConf('CardMonth')
    syear = readConf('CardYear')
    scvv = readConf('CardCVV')

    purchaseItem(sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv)

matchedClothes = []
def purchaseItem(sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv):
    timein = sdrop.split(":")
    returnTime(timein[0])
    url = 'http://www.supremenewyork.com/shop/all/'
    url += scatType
    driver.get(url);
    listings = driver.find_elements_by_class_name("name-link")
    split = skeywords.split(",")
    for splits in split:
        keywords.append(splits)
    for i in range(0, len(listings), 1):
        if i % 2 != 0: 
            text = listings[i-1].text
            split = text.strip().split(" ")
            matches = 0
            colour = 0
            for keyword in keywords:
                for splits in split:
                    if keyword == splits:
                        matches += 1
            coloura = listings[i].text
            if scolour == coloura:
                colour = 1
            if matches != 0:
                matches += colour
            checkedListings.append(matches)
            matchedClothes.append(matches)
    largestMatch = 0
    for i in range(0, len(checkedListings), 1):
        if checkedListings[i] > largestMatch:
            largestMatch = checkedListings[i]

    selectedIndex = 0
    for i in range(0, len(matchedClothes), 1):
        if largestMatch == matchedClothes[i]:
            selectedIndex = i * 2

    listings[selectedIndex].click()

    time.sleep(0.8)

    if sizeC == 1:
        size = Select(driver.find_element_by_id("size"))
        size.select_by_visible_text(ssize)

    try:
        add = driver.find_element_by_xpath("""//*[@id="add-remove-buttons"]/input""")
        add.click()
    except NoSuchElementException:
        print("Sorry the item is sold out!")
        return

    time.sleep(0.5)
    cart = check_exists_by_xpath("""//*[@id="cart"]/a[2]""", driver)
    cart.click()


    name = check_exists_by_xpath("""//*[@id="order_billing_name"]""", driver)
    name.send_keys(sname)

    email = check_exists_by_xpath("""//*[@id="order_email"]""", driver)
    email.send_keys(semail)

    phone = check_exists_by_xpath("""//*[@id="order_tel"]""", driver)
    phone.send_keys(stel)

    add1 = check_exists_by_xpath("""//*[@id="bo"]""", driver)
    add1.send_keys(sadd1)

    add2 = check_exists_by_xpath("""//*[@id="oba3"]""", driver)
    add2.send_keys(sadd2)

    add3 = check_exists_by_xpath("""//*[@id="order_billing_address_3"]""", driver)
    add3.send_keys(sadd3)

    city = check_exists_by_xpath("""//*[@id="order_billing_city"]""", driver)
    city.send_keys(scity)

    country = Select(driver.find_element_by_id("order_billing_country"))
    country.select_by_visible_text(scountry)

    postcode = check_exists_by_xpath("""//*[@id="order_billing_zip"]""", driver)
    postcode.send_keys(spostcode)

    cardType = Select(driver.find_element_by_id("credit_card_type"))
    cardType.select_by_visible_text(scard)

    tickBox = driver.find_element_by_xpath("""//*[@id="cart-cc"]/fieldset/p/label/div/ins""")
    tickBox.click()

    if isPayPal != 1:
        cardno = check_exists_by_xpath("""//*[@id="cnb"]""", driver)
        cardno.send_keys(scardno)

        cvv = check_exists_by_xpath("""//*[@id="vval"]""", driver)
        cvv.send_keys(scvv)

        expiraryDate1 = Select(driver.find_element_by_id("credit_card_month"))
        expiraryDate1.select_by_visible_text(smonth)

        expiraryDate2 = Select(driver.find_element_by_id("credit_card_year"))
        expiraryDate2.select_by_visible_text(syear)
    
    complete = check_exists_by_xpath("""//*[@id="pay"]/input""", driver)
    complete.click()
    print("Complete the captcha and confirm the order manually. Thanks for using my bot ;)")
    print("If this bot helped you make money/cop a nice item, please consider donating on paypal at shaerthomas@gmail.com")

def decr(value):
    m = sha256()
    m.update(password)
    passwd = m.digest()
    iv = m.digest()[::2]
    cipher = aes.AESModeOfOperationCFB(passwd, iv = iv)
    decrypted = cipher.decrypt(b64decode(value))
    return decrypted[:-ord(decrypted[-1:])].decode('ascii')

def encr(value):
    m = sha256()
    m.update(password)
    key = m.digest()
    iv = m.digest()[::2]
    pad = 16 - len(value) % 16
    raw = value + pad * chr(pad)
    cipher = aes.AESModeOfOperationCFB(key, iv = iv)
    return b64encode(cipher.encrypt(raw)).decode('ascii')

def readConf(key):
    config = ConfigParser()
    config.read('config.cnf')
    try:
        return decr(config.get(config.sections()[0], key))
    except TypeError:
        return ''

def writeToConf(key, value):
    config = ConfigParser()
    config.read('config.cnf')
    encValue = encr(value)
    config.set(config.sections()[0], key, encValue)
    cfgfile = open('config.cnf', 'w')
    config.write(cfgfile)
    cfgfile.close()

print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
print("Thanks for using my bot. Please note this bot is experimental and in a very early development stage. \n")
print("This bot is simply a script. By deciding to use this bot you are responsible for any purchases. Not me. \n")
print("PLEASE ENTER THE CORRECT PATH TO YOUR CHROME.EXE IN THE 'chromepath.txt' FILE \n")
print("Also note that the bot will likely cause a RECAPTCHA to appear. Please be prepared to quickly solve it and confirm the order.")
print("If you have any questions please feel free to contact me at shaerthomas@gmail.com, or post on the reddit thread. \n")
print("HA6")
print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

print("\n Start filling in the details while the page loads should take ~30 seconds. If the page takes too longer then this restart the page.")
print("\n Fill out all the details, make sure you get all of them right. If you need help please open 'readme.txt' or check the reddit post.")

useConfig = False
if not os.path.isfile('config.cnf'):
    config = ConfigParser()
    config.add_section('SupremeBotConfig')
    for x in paydetails:
        config.set('SupremeBotConfig', x, ' ')
    cfgfile = open('config.cnf', 'w')
    config.write(cfgfile)
    cfgfile.close()
    useConfig = False
else:
    inp = input('Do you want to use the stored payment details? (Yes/No) ')
    if 'YES' in inp.upper() or 'Y' in inp.upper():
        useConfig = True
        inp = input('\nEnter your password to continue: ')
        password = inp.encode('ascii')
    else:
        useConfig = False


def openPage():
    rawPath = os.getcwd()
    a = rawPath.replace("\\", "/")
    if not useConfig:
        a += "/details.html"
    else:
        a += "/details2.html"
    driver.get(a)
    driver.set_page_load_timeout(5)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    if not useConfig:
        readDetails()
    else:
        readProduct()
    
openPage()

    

'''
openChrome()
'''
