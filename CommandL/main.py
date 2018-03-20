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
import win32com.client as comclt
import datetime
import re
import sys
from datetime import datetime
import pytz

import encrypt as enc

LOGFILE = True

paydetails = OrderedDict(
    [('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''),
     ('Addr3', ''),
     ('City', ''), ('Post/zip code', ''), ('Country', ''), ('Cardno', ''),
     ('CardCVV', ''),
     ('CardMonth', ''), ('CardYear', ''), ('CardType', '')])

categoryList = ['jackets', 'shirts', 'tops/sweaters', 'sweatshirts', 'pants', 'hats', 'bags',
                'accessories', 'shoes', 'skate']

checkedListings = []

password = b'insecure password'


def readPath():
    f = open("chromepath.txt", "r").readlines()
    makeitastring = ''.join(map(str, f))
    return makeitastring


def writeLog(txt):
    if not LOGFILE:
        return None
    f = open('logfile.txt', 'a')
    f.write(str(txt) + '\n')
    f.close()


def selectSize():
    global sizeC
    sizeC = 0
    sizes = ["Small", "Medium", "Large", "XLarge"]
    print("Select Size (Alternatively simply enter 'D' for the first available size)")
    if selectedCategory == "jackets" or selectedCategory == "shirts" or selectedCategory == "tops/sweaters" or selectedCategory == "sweatshirts":
        string = "Possible Sizes for "
        string += selectedCategory
        string += ": Small, Medium, Large, XLarge"
        print(string)
        sizeInput = input("Select size: ")
        if sizeInput in sizes:
            return sizeInput
        elif sizeInput == "D":
            sizeC = 1
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
            sizeC = 1
        else:
            print("Please enter a correctly formated size")
            return selectSize()

    else:
        sizeInput = input("Select size: ").title()
        if sizeInput == "D":
            sizeC = 1
        elif sizeInput != "D":
            sizeC = 2
        return sizeInput


def selectColour():
    colour = input("Select a colour/model (please use a capital letter e.g. Black/Red/Blue) ").title()
    answer = input("Are you sure about the settings? [Y]es/[N]o: ").upper()
    if answer == "Y":
        return colour
    elif answer == "N":
        return selectColour()


def listOptions():
    print("-------------------------------------")
    category = "Selected Category: "
    category += selectedCategory
    print(category)
    print("Selected Keywords: ")
    print(keywords)
    print("Selected Size: ")
    print(selectedSize)
    colour = "Selected Colour: "
    colour += selectedColour
    print(colour)
    print("Please make sure all of these values are correct. If they are not please restart the program and try again.")
    print("If you have any questions please view the respective reddit post or email me at shaerthomas@gmail.com")
    print("-------------------------------------\n")


def check_exists_by_xpath(xpath, driver):
    try:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        myElem = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return driver.find_element_by_xpath(xpath)


def returnTime():
    timeS = "Please enter the hour of the drop (e.g. if you're in the UK enter '11' for 11.00am) "

    isTime = input(timeS)
    dropTime = int(isTime)
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
    if len(value) <= 1:
        return None
    try:
        driver.execute_script("arguments[0].value = '" + value + "';", field)
    except WebDriverException:
        pass


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


def openChrome():
    matchedClothes = []
    service.start()
    driver = webdriver.Remote(service.service_url, capabilities)

    inp = input('Do you want to use strict item selection? [Y]es/[N]o: ')
    if inp.upper() == 'YES' or inp.upper() == 'Y':
        loop = True
    else:
        loop = False

    returnTime()
    while True:
        url = 'http://www.supremenewyork.com/shop/all/'
        url += selectedCategory
        driver.get(url)

        listings = driver.find_elements_by_class_name("name-link")

        for i in range(0, len(listings), 1):
            if i % 2 != 0:
                text = listings[i - 1].text
                split = text.strip()
                matches = 0
                colour = 0
                for keyword in keywords:
                    if keyword.encode('ascii', 'ignore') in split.encode('ascii', 'ignore'):
                        matches += 1
                coloura = listings[i].text
                if selectedColour.encode('ascii', 'ignore') == coloura.encode('ascii', 'ignore'):
                    colour = 1
                if matches != 0:
                    matches += colour
                writeLog([keywords, split, selectedColour, coloura, matches])
                checkedListings.append(matches)
                matchedClothes.append(matches)
        largestMatch = 0
        for i in range(0, len(checkedListings), 1):
            if checkedListings[i] > largestMatch:
                largestMatch = checkedListings[i]
        if selectedColour != '' and largestMatch == len(keywords) + 1:
            break
        elif selectedColour == '' and largestMatch == len(keywords):
            break
        elif not loop:
            break

    selectedIndex = 0
    for i in range(0, len(matchedClothes), 1):
        if largestMatch == matchedClothes[i]:
            selectedIndex = i * 2
            writeLog(selectedIndex)

    listings[selectedIndex].click()

    time.sleep(0.8)

    try:
        if sizeC != 1:
            size = Select(driver.find_element_by_id("size"))
            op = size.options
            found = False
            for x in op:
                if selectedSize in x.text:
                    found = True
                    break
            if found:
                selectText(selectedSize, size)
            else:
                print("Sorry the item size is sold out!")
                return None
            
            
        add = driver.find_element_by_xpath("""//*[@id="add-remove-buttons"]/input""")
        add.click()
    except NoSuchElementException:
        print("Sorry the item is sold out!")
        return

    time.sleep(0.5)
    cart = check_exists_by_xpath("""//*[@id="cart"]/a[2]""", driver)
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

    add3 = check_exists_by_xpath("""//*[@id="order_billing_address_3"]""", driver)
    sendKeys(paydetails['Addr3'], add3, driver)

    city = check_exists_by_xpath("""//*[@id="order_billing_city"]""", driver)
    sendKeys(paydetails['City'], city, driver)

    postcode = check_exists_by_xpath("""//*[@id="order_billing_zip"]""", driver)
    sendKeys(paydetails['Post/zip code'], postcode, driver)

    country = Select(driver.find_element_by_id("order_billing_country"))
    selectText(paydetails['Country'], country, True)

    if paydetails['CardType'] != 1:
        cardno = check_exists_by_xpath("""//*[@id="cnb"]""", driver)
        sendKeys(paydetails['Cardno'], cardno, driver)

        cvv = check_exists_by_xpath("""//*[@id="vval"]""", driver)
        sendKeys(paydetails['CardCVV'], cvv, driver)

        cardType = Select(driver.find_element_by_id("credit_card_type"))
        selectText(paydetails['CardType'], cardType)

        expiraryDate1 = Select(driver.find_element_by_id("credit_card_month"))
        selectText(paydetails['CardMonth'], expiraryDate1)

        expiraryDate2 = Select(driver.find_element_by_id("credit_card_year"))
        selectText(paydetails['CardYear'], expiraryDate2)

    tickBox = driver.find_element_by_xpath("""//*[@id="cart-cc"]/fieldset/p/label/div/ins""")
    tickBox.click()

    complete = check_exists_by_xpath("""//*[@id="pay"]/input""", driver)
    complete.click()
    print("Complete the captcha and confirm the order manually. Thanks for using me ;)")
    print("If this bot helped you make money/cop a nice item, please consider donating to a charity of your choice")


def selectKeywords():
    global keywords
    keywords = []
    keywordsInput = input("Select keywords, use a comma to separate tags e.g. Reflective,Sleeve,Logo,Puffer \n")
    for splits in keywordsInput.strip().replace(" ", "").title().split(","):
        keywords.append(splits)


def selectCategory():
    categoryInput = input(
        "Select type: jackets, shirts, tops/sweaters, sweatshirts, pants, hats, bags, accessories, shoes, skate\n").lower()
    if categoryInput.lower() in categoryList:
        selected = categoryInput.lower()
        print('Selected Category: %s' % (selected))
        return selected
    else:
        print("Please enter one of the listed categories exactly")
        return selectCategory()


def getPDetails():
    global password
    for x in paydetails:
        paydetails[x] = input('Enter %s: ' % (x))

    inp = input('\n\nDo you want to safe your details encrypted for easy future use? [Y]es/[N]o: ')
    if inp.upper() == 'YES' or inp.upper() == 'Y':
        inp = input('Enter a password: ')
        enc.password = inp.encode('ascii')
        for x in paydetails:
            enc.writeToConf(x, paydetails[x])


def confirmPayDetails():
    print("-------------------------------------")
    print("Billing information and address.")
    for x in paydetails:
        print(x + ':' + ' ' * int(15 - len(x)) + paydetails[x])
    print("-------------------------------------")
    inp = input('Is this information correct? [Y]es/[N]o: ')
    if inp.upper() == 'NO' or inp.upper() == 'N':
        return False
    elif inp.upper() == 'YES' or inp.upper() == 'Y':
        return True
    else:
        return confirmPayDetails()


def main():
    global service
    global selectedCategory
    global selectedSize
    global selectedColour
    global capabilities
    global password
    wsh = comclt.Dispatch("WScript.Shell")
    chromePath = readPath()

    service = service.Service('chromedriver.exe')
    capabilities = {'chrome.binary': chromePath}

    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print("Thanks for using our bot. Please note this bot is experimental and in a very early development stage.")
    print("This bot is simply a script. By deciding to use this bot you are responsible for any purchases. Not us.")
    print("PLEASE ENTER THE CORRECT PATH TO YOUR CHROME.EXE IN THE 'chromepath.txt' FILE")
    print("Read the README.md file carefully before use")
    print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
    print(
        "\nFill out all the details, make sure you get all of them right. If you need help please open 'README.md' or check the reddit post.")

    if not path.isfile('config.cnf'):
        enc.paydetails = paydetails
        enc.initConf()
        getPDetails()
    else:
        inp = input('Do you want to use your stored details? [Y]es/[N]o: ')
        if inp.upper() == 'YES' or inp.upper() == 'Y':
            inp = input('Enter your password: ')
            enc.password = inp.encode('ascii')
            for x in paydetails:
                paydetails[x] = enc.readConf(x)
        else:
            getPDetails()

    if not confirmPayDetails():
        getPDetails()

    selectedCategory = selectCategory()
    selectKeywords()

    selectedSize = selectSize()
    selectedColour = selectColour()
    listOptions()
    openChrome()


if __name__ == '__main__':
    main()
