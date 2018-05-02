from configparser import ConfigParser
from collections import OrderedDict
from os import path
from collections import OrderedDict
import time
import openpyxl
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
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import Proxy, ProxyType
import win32com.client as comclt
import datetime, re, sys
from random import random
from datetime import datetime
import pytz

import encrypt as enc

LOGFILE = True

EUpDescr = {'Country': '(UK, DE, FR, ...)', 'CardMonth': '(01, 02, ..., 12)', 'Name': '(first and last name)', 'CardType': '(or enter "Paypal")'}
USpDescr = {'Country': '(USA or CANADA)', 'CardMonth': '(01, 02, ..., 12)', 'Name': '(first and last name)', 'Addr3': '(State abbreviation: AL, AK, AS, ...)'}

paydetails = OrderedDict(
    [('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''), ('Addr3', ''),
     ('City', ''), ('Post/zip code', ''), ('Country', ''), ('CardType', ''), ('Cardno', ''),
     ('CardCVV', ''), ('CardMonth', ''), ('CardYear', '')])

categoryList = ['jackets', 'shirts', 'tops_sweaters', 'sweatshirts', 'pants', 'hats', 'bags',
                'accessories', 'shoes', 'skate']

checkedListings = []

password = b'insecure password'


def pause():
    time.sleep(random())


def getLoc(f):
    loc = path.dirname(__file__)
    if len(loc) < 1:
        return f
    return loc + '\\' + f


def readPath():
    f = open(getLoc("chromepath.txt"), "r").readlines()
    makeitastring = ''.join(map(str, f))
    return makeitastring


def writeLog(txt):
    if not LOGFILE:
        return None
    f = open(getLoc('logfile.txt'), 'a')
    f.write(str(txt) + '\n')
    f.close()


def selectSize():
    sizeC = 0
    sizes = ["Small", "Medium", "Large", "XLarge"]
    print("Select Size (Alternatively simply enter 'D' for the first available size)")
    if selectedCategory == "jackets" or selectedCategory == "shirts" or selectedCategory == "tops_sweaters" or selectedCategory == "sweatshirts":
        string = "Possible Sizes for "
        string += selectedCategory
        string += ": Small, Medium, Large, XLarge"
        print(string)
        sizeInput = input("Select size: ")
        if sizeInput in sizes:
            return sizeInput
        elif sizeInput == "D":
            return sizeInput
        else:
            print("Please enter one of the listed sizes exactly")
            print(sizeInput)
            return selectSize()
    elif selectedCategory == "shoes":
        string = "Size format "
        string += selectedCategory
        string += ": US 9 / UK 8, US 9.5 / UK 8.5, US 10 / UK 9"
        print(string)
        sizeInput = input("Select size: ")
        if 'US ' in sizeInput and ' / UK ' in sizeInput:
            return sizeInput
        elif sizeInput == "D":
            return sizeInput
        else:
            print("Please enter a correctly formated size")
            return selectSize()

    else:
        sizeInput = input("Select size: ").title()
        return sizeInput


def selectColour():
    colour = input("Select a colour/model (please use a capital letter e.g. Black/Red/Blue) ").title()
    return colour


def listOptions(cat, key, size, col):
    print("\n-------------------------------------")
    print('Selected category: ' + cat)
    print('Selected keywords: ' + key)
    print('Selected size:     ' + size)
    print('Selected colour:   ' + col)
    print("-------------------------------------\n")


def check_exists_by_xpath(xpath, driver):
    try:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)


def returnTime():
    timeEU = "Please enter the hour of the drop (e.g. if you're in the UK enter '11' for 11.00am) "
    timeUS = "Please enter the hour of the drop "
    if reg == 'EU':
        timeS = timeEU
    elif reg == 'US':
        timeS = timeUS

    isTime = input(timeS)
    if len(isTime) < 0:
        print('Invalid input')
        sys.exit(1)
    try:
        dropTime = int(isTime)
    except:
        print('Invalid input')
        sys.exit(1)
    text = "Drop selected for "
    text += isTime
    text += ":00"
    text += " the program will automatically run at this time. Please do not close the web browser or cmd box."
    print(text)
    while True:
        ts = time.time()
        houra = datetime.fromtimestamp(ts).strftime('%H')
        hour = int(houra)
        if hour >= dropTime:
            time.sleep(1)
            break


def sendKeys(value, field, driver):
    if len(value) < 1:
        return None
    try:
        driver.execute_script("arguments[0].value = '" + value + "';", field)
    except WebDriverException:
        print(field.get_attribute('Name'))


def selectText(value, obj, attr=False):
    if attr:
        try:
            obj.select_by_value(value)
        except WebDriverException:
            return None
    try:
        obj.select_by_visible_text(value)
    except WebDriverException:
        return None


def searchItem(item):
    url = 'http://www.supremenewyork.com/shop/all/'
    url += item['selectedCategory']

    while True:
        matchedClothes = []
        checkedListings = []
        driver.get(url)

        listings = driver.find_elements_by_class_name("name-link")
        for i in range(0, len(listings), 1):
            if i % 2 != 0:
                text = listings[i - 1].text
                split = text.strip()
                matches = 0
                colour = 0
                for keyword in item['keywords']:
                    if keyword.encode('ascii', 'ignore') in split.encode('ascii', 'ignore'):
                        matches += 1
                try:
                    coloura = listings[i].text
                    if item['selectedColour'].encode('ascii', 'ignore') in coloura.encode('ascii', 'ignore'):
                        colour = 1
                except AttributeError:
                    colour = 0
                if matches != 0:
                    matches += colour
                writeLog([item['keywords'], split, item['selectedColour'], coloura, matches, len(item['keywords']) + 1])
                checkedListings.append(matches)
                matchedClothes.append(matches)

        largestMatch = 0
        for i in range(0, len(checkedListings), 1):
            if checkedListings[i] > largestMatch:
                largestMatch = checkedListings[i]
        if item['selectedColour'] != '' and largestMatch == len(item['keywords']) + 1:
            break
        elif item['selectedColour'] == '' and largestMatch == len(item['keywords']):
            break
        elif not strict:
            break

    selectedIndex = 0
    for i in range(0, len(matchedClothes), 1):
        if largestMatch == matchedClothes[i]:
            selectedIndex = i * 2
            writeLog(selectedIndex)

    listings[selectedIndex].click()

    time.sleep(0.5+random())

    try:
        if item['selectedSize'] != 'D':
            if reg == 'EU':
                size = Select(driver.find_element_by_id("size"))
            elif reg == 'US':
                size = Select(driver.find_element_by_id("s"))
            op = size.options
            found = False
            for x in op:
                if item['selectedSize'] in x.text:
                    found = True
                    break
            if found:
                selectText(item['selectedSize'], size)
            else:
                print("Sorry the item size is sold out!")
                return None

        add = driver.find_element_by_xpath("""//*[@id="add-remove-buttons"]/input""")
        add.click()
    except NoSuchElementException:
        print("Sorry the item is sold out!")
        return None
    pause()    


def openChrome():
    global driver, strict
    service.start()
    driver = webdriver.Remote(service.service_url, capabilities)

    inp = input('Do you want to use strict item selection? [Y]es/[N]o: ')
    if inp.upper() == 'YES' or inp.upper() == 'Y':
        strict = True
    else:
        strict = False

    returnTime()
    for it in items:
        searchItem(it)
        


def cart():
    cart = driver.find_elements_by_class_name('checkout')[0]
    cart.click()

    name = check_exists_by_xpath("""//*[@id="order_billing_name"]""", driver)
    sendKeys(paydetails['Name'], name, driver)

    email = check_exists_by_xpath("""//*[@id="order_email"]""", driver)
    sendKeys(paydetails['Email'], email, driver)

    phone = check_exists_by_xpath("""//*[@id="order_tel"]""", driver)
    sendKeys(paydetails['Phone'], phone, driver)

    add1 = check_exists_by_xpath("""//*[@id="bo"]""", driver)
    sendKeys(paydetails['Addr1'], add1, driver)

    add2 = check_exists_by_xpath("""//*[@id="oba3"]""", driver)
    sendKeys(paydetails['Addr2'], add2, driver)

    country = Select(driver.find_element_by_name("order[billing_country]"))
    selectText(paydetails['Country'], country, True)

    if reg == 'EU':
        add3 = check_exists_by_xpath("""//*[@id="order_billing_address_3"]""", driver)
        sendKeys(paydetails['Addr3'], add3, driver)
    elif reg == 'US':
        state = Select(driver.find_element_by_name("order[billing_state]"))
        selectText(paydetails['Addr3'], state, True)

    city = check_exists_by_xpath("""//*[@id="order_billing_city"]""", driver)
    sendKeys(paydetails['City'], city, driver)

    postcode = check_exists_by_xpath("""//*[@id="order_billing_zip"]""", driver)
    sendKeys(paydetails['Post/zip code'], postcode, driver)

    if reg == 'EU':
        cardType = Select(driver.find_element_by_id("credit_card_type"))
        selectText(paydetails['CardType'].lower(), cardType, True)

    if paydetails['CardType'].lower() != 'paypal':
        if reg == 'EU':
            cardno = check_exists_by_xpath("""//*[@id="cnb"]""", driver)
        elif reg == 'US':
            cardno = check_exists_by_xpath("""//*[@id="nnaerb"]""", driver)
        sendKeys(paydetails['Cardno'], cardno, driver)

        if reg == 'EU':
            cvv = check_exists_by_xpath("""//*[@id="vval"]""", driver)
        elif reg == 'US':
            cvv = check_exists_by_xpath("""//*[@id="orcer"]""", driver)
        sendKeys(paydetails['CardCVV'], cvv, driver)

        expiraryDate1 = Select(driver.find_element_by_name("credit_card[month]"))
        selectText(paydetails['CardMonth'], expiraryDate1, True)

        expiraryDate2 = Select(driver.find_element_by_name("credit_card[year]"))
        selectText(paydetails['CardYear'], expiraryDate2, True)

    tickBox = driver.find_element_by_xpath("""//*[@id="cart-cc"]/fieldset/p/label/div/ins""")
    tickBox.click()

    complete = check_exists_by_xpath("""//*[@id="pay"]/input""", driver)
    #complete.click()
    print("Complete the captcha and confirm the order manually. Thanks for using me ;)")
    print("If this bot helped you make money/cop a nice item, please consider donating to a charity of your choice")


def selectKeywords():
    keywords = []
    keywordsInput = input("Select keywords, use a comma to separate tags e.g. Reflective,Sleeve,Logo,Puffer \n")
    for splits in keywordsInput.strip().replace(" ", "").title().split(","):
        keywords.append(splits)
    return keywords


def selectCategory():
    categoryInput = input(
        "Select type: jackets, shirts, tops_sweaters, sweatshirts, pants, hats, bags, accessories, shoes, skate\n").lower()
    if categoryInput.lower() in categoryList:
        selected = categoryInput.lower()
        print('Selected Category: %s' % (selected))
        return selected
    else:
        print("Please enter one of the listed categories exactly")
        return selectCategory()


def getPDetails():
    global password
    pp = False
    for x in paydetails:
        if (reg == 'US' and x == 'CardType') or (pp and (x == 'Cardno' or x == 'CardCVV' or x == 'CardMonth' or x == 'CardYear')):
            paydetails[x] = 'Not Used'
        elif x in pDescr:
            paydetails[x] = input('Enter %s %s: ' % (x, pDescr[x]))
        else:
            paydetails[x] = input('Enter %s: ' % (x))
        if reg == 'EU' and paydetails['CardType'].lower() == 'paypal':
            pp = True

    inp = input('\n\nDo you want to safe your details encrypted for easy future use? [Y]es/[N]o: ')
    if inp.upper() == 'YES' or inp.upper() == 'Y':
        inp = input('Enter a password: ')
        enc.password = inp.encode('ascii')
        for x in paydetails:
            enc.writeToConf(x, paydetails[x])


def confirmPayDetails():
    print("\n-------------------------------------")
    print("Billing information and address.")
    for x in paydetails:
        print(x + ':' + ' ' * int(15 - len(x)) + paydetails[x])
    print("-------------------------------------\n")
    inp = input('Is this information correct? [Y]es/[N]o: ')
    if inp.upper() == 'NO' or inp.upper() == 'N':
        return False
    elif inp.upper() == 'YES' or inp.upper() == 'Y':
        return True
    else:
        return confirmPayDetails()


def selectItemNum():
    global itemNum
    inp = input('How many items do you want?:  ')
    if inp.isnumeric():
        itemNum = int(inp)
    else:
        print('Invalid input')
        sys.exit(1)


def getItemDetails():
    global items, selectedCategory
    while True:
        #selectedCategory = selectCategory()
        selectedCategory = 'jackets'
        #keywords = selectKeywords()
        keywords = ['World', 'Famous']

        #selectedSize = selectSize()
        selectedSize = 'D'
        #selectedColour = selectColour()
        selectedColour = 'Green'

        listOptions(selectedCategory, ','.join(keywords), selectedSize, selectedColour)
        answer = input("Are you sure about these settings? [Y]es/[N]o: ").upper()
        if answer == "Y":
            break
  
    items.append({'selectedCategory': selectedCategory, 'keywords': keywords, 'selectedSize': selectedSize, 'selectedColour': selectedColour})
    

def getRegion():
    inp = input('Enter region (EU or US): ')
    if inp.upper() == 'EU':
        return 'EU'
    elif inp.upper() == 'US':
        return 'US'
    else:
        return getRegion()


def main():
    global service, capabilities, password, items, reg, pDescr
    wsh = comclt.Dispatch("WScript.Shell")
    chromePath = readPath()

    service = service.Service(getLoc('chromedriver.exe'))
    capabilities = {'chrome.binary': chromePath}

    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print("Thanks for using our bot. Please note this bot is experimental and in a very early development stage.")
    print("This bot is simply a script. By deciding to use this bot you are responsible for any purchases. Not us.")
    print("PLEASE ENTER THE CORRECT PATH TO YOUR CHROME.EXE IN THE 'chromepath.txt' FILE")
    print("Read the README.md file carefully before use")
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print(
        "\nFill out all the details, make sure you get all of them right. If you need help please open 'README.md' or check the reddit post.")

    reg = getRegion()

    if reg == 'EU':
        pDescr = EUpDescr
    elif reg == 'US':
        pDescr = USpDescr
    
    if not path.isfile(getLoc('config.cnf')):
        enc.paydetails = paydetails
        enc.initConf()
        getPDetails()
    else:
        inp = input('Do you want to use your stored details? [Y]es/[N]o: ')
        enc.update(paydetails)
        if inp.upper() == 'YES' or inp.upper() == 'Y':
            inp = input('Enter your password: ')
            enc.password = inp.encode('ascii')
            for x in paydetails:
                paydetails[x] = enc.readConf(x)
        else:
            getPDetails()

    if not confirmPayDetails():
        getPDetails()

    selectItemNum()

    items = []
    for x in range(itemNum):
        getItemDetails()

    openChrome()
    cart()


if __name__ == '__main__':
    main()
