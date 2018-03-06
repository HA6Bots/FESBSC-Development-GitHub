import os.path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import encrypt as enc


isPayPal = 0
checkedListings = []
sizeC = 0
keywords = []
matchedClothes = []

useConfig = False
password = ''

def openPage(driver):
    rawPath = os.getcwd()
    a = rawPath.replace("\\", "/")
    if not useConfig:
        a += "/details.html"
    else:
        a += "/details2.html"
    driver.get(a)
    if not useConfig:
        readDetails(driver)
    else:
        readProduct(driver, password)


def check_exists_by_xpath_no_wait(xpath, driver):
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

def readDetailsFromList(driver, xpath):
    details = driver.find_elements_by_xpath(xpath)
    detail = details[0].text
    if len(details) > 1:
        detail = (details[len(details) - 1].text)
        print(detail)
        return detail
    elif len(details) <= 1:
        print(detail)
        return detail


def readProduct(driver, password):
    input("Fill out the details and click the button when finished. Then, press enter to continue.")

    sdrop = readDetailsFromList(driver, """//*[@id="drop_time"]""")
    scatType = readDetailsFromList(driver, """//*[@id="category_type"]""")
    scolour = readDetailsFromList(driver, """//*[@id="colour"]""")
    skeywords = readDetailsFromList(driver, """//*[@id="order_keywords"]""")
    ssize = readDetailsFromList(driver, """//*[@id="size"]""")


    sname = enc.readConf('Name', password)
    semail = enc.readConf('Email', password)
    stel = enc.readConf('Phone', password)
    sadd1 = enc.readConf('Addr1', password)
    sadd2 = enc.readConf('Addr2', password)
    sadd3 = enc.readConf('Addr3', password)
    scity = enc.readConf('City', password)
    spostcode = enc.readConf('Post/zip code', password)
    scountry = enc.readConf('Country', password)
    scard = enc.readConf('CardType', password)
    scardno = enc.readConf('Cardno', password)
    smonth = enc.readConf('CardMonth', password)
    syear = enc.readConf('CardYear', password)
    scvv = enc.readConf('CardCVV', password)

    purchaseItem(driver, sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv)


def findItemByIndex(listings, skeywords, scolour):
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

    return selectedIndex


def purchaseItem(driver, sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv):
    timein = sdrop.split(":")
    print(timein[0])
    returnTime(timein[0])
    url = 'http://www.supremenewyork.com/shop/all/'
    url += scatType
    driver.get(url);
    listings = driver.find_elements_by_class_name("name-link")
    listings[findItemByIndex(listings, skeywords, scolour)].click()

    time.sleep(2)

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

def readDetails(driver):
    global password
    print("Page loaded! Do you want to safe your credentials encrypted for later use? (yes/no) ")
    ready = input()
    if ready.upper() == "YES" or ready.upper() == "Y":
        safeConf = True
    else:
        safeConf = False

    sname = readDetailsFromList(driver, """//*[@id="name"]""")
    semail = readDetailsFromList(driver, """//*[@id="order_email"]""")
    stel = readDetailsFromList(driver, """//*[@id="order_tel"]""")
    sadd1 = readDetailsFromList(driver, """//*[@id="bo"]""")

    sadd2 = ""
    if check_exists_by_xpath_no_wait("""//*[@id="oba3"]""", driver) == True:
        sadd2 = readDetailsFromList(driver, """//*[@id="oba3"]""")

    sadd3 = ""
    if check_exists_by_xpath_no_wait("""//*[@id="order_billing_address_3"]""", driver) == True:
        sadd3 = readDetailsFromList(driver, """//*[@id="order_billing_address_3"]""")

    scity = readDetailsFromList(driver, """//*[@id="order_billing_city"]""")
    spostcode = readDetailsFromList(driver, """//*[@id="order_billing_zip"]""")
    scountry = readDetailsFromList(driver, """//*[@id="order_billing_country"]""")
    scard = readDetailsFromList(driver, """//*[@id="credit_card_type"]""")

    if scard == "American":
        scard = "American Express"
    if scard == "PayPal":
        isPayPal = 1

    scardno = readDetailsFromList(driver, """//*[@id="cnb"]""")
    smonth = readDetailsFromList(driver, """//*[@id="credit_card_month"]""")
    syear = readDetailsFromList(driver, """//*[@id="credit_card_year"]""")
    sdrop = readDetailsFromList(driver, """//*[@id="drop_time"]""")
    scatType = readDetailsFromList(driver, """//*[@id="category_type"]""")
    scolour = readDetailsFromList(driver, """//*[@id="colour"]""")
    skeywords = readDetailsFromList(driver, """//*[@id="order_keywords"]""")
    ssize = readDetailsFromList(driver, """//*[@id="size"]""")
    scvv = readDetailsFromList(driver, """//*[@id="vval"]""")

    if safeConf:
        inp = input("\nEnter a password to continue")
        password = inp.encode('ascii')
        enc.writeToConf('Name', sname, password)
        enc.writeToConf('Email', semail, password)
        enc.writeToConf('Phone', stel, password)
        enc.writeToConf('Addr1', sadd1, password)
        enc.writeToConf('Addr2', sadd2, password)
        enc.writeToConf('Addr3', sadd3, password)
        enc.writeToConf('City', scity, password)
        enc.writeToConf('Post/zip Code', spostcode, password)
        enc.writeToConf('Country', scountry, password)
        enc.writeToConf('Cardno', scardno, password)
        enc.writeToConf('CardCVV', scvv, password)
        enc.writeToConf('CardMonth', smonth, password)
        enc.writeToConf('CardYear', syear, password)
        enc.writeToConf('CardType', scard, password)

        purchaseItem(driver, sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv)
    purchaseItem(driver, sname, semail, stel, sadd1, sadd2, sadd3, scity, spostcode, scountry, scard, scardno, smonth, syear, sdrop, scatType, scolour, skeywords, ssize, scvv)

def intro():
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


