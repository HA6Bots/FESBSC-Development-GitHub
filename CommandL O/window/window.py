import sys, os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import encrypt as enc
from collections import OrderedDict



paydetails = OrderedDict(
    [('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''), ('Addr3', ''),
     ('City', ''), ('Post/zip code', ''), ('Country', ''), ('CardType', ''), ('Cardno', ''),
     ('CardCVV', ''), ('CardMonth', ''), ('CardYear', ''), ('Region', '')])

categoryList = ['jackets', 'shirts', 'tops_sweaters', 'sweatshirts', 'pants', 'hats', 'bags',
                'accessories', 'shoes', 'skate']


#MAJOR TO DO
#send output into main program
#allow to save
#finish region picking

#MINOR TO DO
#CLEAN THIS DIRTY ASS CODE
#set window icon to logo



class App(QWidget):
 
    def __init__(self, isPasswordExists):
        super().__init__()
        self.countryO = ""
        self.title = 'FESBSC 3.0'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        layout = QGridLayout()        
        self.setLayout(layout)
        self.loadBanner()
        self.passwordCheck(isPasswordExists)
        self.shipArea()
        self.orderArea()
        self.initUI()

    #loads the image and text
    def loadBanner(self):
        logo = QLabel(self)
        logo.setGeometry(10, 30, 300, 100)
        pixmap = QPixmap(QtGui.QPixmap(os.getcwd() + "/window/Pictures/title.png"))
        logo.setPixmap(pixmap)

        newFont = QtGui.QFont("Times", 15)
        newFont.setItalic(True)
        free = QLabel("Free", self)
        free.setFont(newFont)
        free.setGeometry(400, 20, 80, 50)

        experimental = QLabel("Experimental", self)
        experimental.setFont(newFont)
        experimental.setGeometry(400, 50, 120, 50)

        supreme = QLabel("Supreme", self)
        supreme.setFont(newFont)
        supreme.setGeometry(400, 80, 120, 50)

        bot = QLabel("Bot", self)
        bot.setFont(newFont)
        bot.setGeometry(400, 110, 80, 50)


        fortheFont = QtGui.QFont("Times", 8)
        fortheFont.setItalic(True)
        
        forthe = QLabel("For The", self)
        forthe.setFont(fortheFont)
        forthe.setGeometry(400, 135, 80, 50)

        supreme2 = QLabel("Supreme", self)
        supreme2.setFont(newFont)
        supreme2.setGeometry(400, 155, 120, 50)

        community = QLabel("Community", self)
        community.setFont(newFont)
        community.setGeometry(400, 180, 120, 50)

        line = QFrame(self);
        line.setGeometry(QRect(0, 240, self.width, 3));
        line.setFrameShape(QFrame.HLine);
        line.setFrameShadow(QFrame.Sunken);

    #populates the months list
    def populateMonths(self):
        for x in range(0, 13):
            y = "0" + str(x)
            if x > 9:
                y = str(x)
            self.month.addItem(y)

    #populates the years list
    def populateYears(self):
        for x in range(0, 11):
            y = 2018 + x
            self.year.addItem(str(y))

    #populates country list
    def populateCountry(self, region):
        self.country.clear()
        if region == "eu":
            #needs to be put in a category
            self.country.addItem("UK")
            self.country.addItem("UK+Ireland")
            self.country.addItem("AT")
            self.country.addItem("BY")
            self.country.addItem("BE")
            self.country.addItem("BG")
            self.country.addItem("HR")
            self.country.addItem("CZ")
            self.country.addItem("DK")
            self.country.addItem("EE")
            self.country.addItem("FI")
            self.country.addItem("FR")
            self.country.addItem("DE")
            self.country.addItem("GR")
            self.country.addItem("HU")
            self.country.addItem("IS")
            self.country.addItem("IE")
            self.country.addItem("IT")
            self.country.addItem("LV")
            self.country.addItem("LT")
            self.country.addItem("LU")
            self.country.addItem("MC")
            self.country.addItem("NL")
            self.country.addItem("NO")
            self.country.addItem("PL")
            self.country.addItem("PT")
            self.country.addItem("RO")
            self.country.addItem("RU")
            self.country.addItem("SK")
            self.country.addItem("SI")
            self.country.addItem("ES")
            self.country.addItem("SE")
            self.country.addItem("CH")
            self.country.addItem("TR")

        elif region == "us":
            self.country.addItem("USA")
            self.country.addItem("CANADA")
        elif region == "asia":
            self.country.addItem("北海道")
            self.country.addItem("青森県")
            self.country.addItem("岩手県")
            self.country.addItem("宮城県")
            self.country.addItem("秋田県")
            self.country.addItem("山形県")
            self.country.addItem("福島県")
            self.country.addItem("茨城県")
            self.country.addItem("栃木県")
            self.country.addItem("群馬県")
            self.country.addItem("埼玉県")
            self.country.addItem("千葉県")
            self.country.addItem("東京都")
            self.country.addItem("神奈川県")
            self.country.addItem("新潟県")
            self.country.addItem("富山県")
            self.country.addItem("石川県")
            self.country.addItem("福井県")
            self.country.addItem("山梨県")
            self.country.addItem("長野県")
            self.country.addItem("岐阜県")
            self.country.addItem("静岡県")
            self.country.addItem("愛知県")
            self.country.addItem("三重県")
            self.country.addItem("滋賀県")
            self.country.addItem("京都府")
            self.country.addItem("大阪府")
            self.country.addItem("兵庫県")
            self.country.addItem("奈良県")
            self.country.addItem("和歌山県")
            self.country.addItem("鳥取県")
            self.country.addItem("島根県")
            self.country.addItem("岡山県")
            self.country.addItem("広島県")
            self.country.addItem("山口県")
            self.country.addItem("徳島県")
            self.country.addItem("香川県")
            self.country.addItem("愛媛県")
            self.country.addItem("高知県")
            self.country.addItem("福岡県")
            self.country.addItem("佐賀県")
            self.country.addItem("長崎県")
            self.country.addItem("熊本県")
            self.country.addItem("大分県")
            self.country.addItem("宮崎県")
            self.country.addItem("鹿児島県")
            self.country.addItem("沖縄県")


    def populatePType(self, region):
        self.payType.clear()
        if region == "eu":
            self.payType.addItem("Visa")
            self.payType.addItem("American Express")
            self.payType.addItem("Mastercard")
            self.payType.addItem("Solo")
            self.payType.addItem("PayPal") #NOTE dont load card details
        elif region == "asia":
            self.payType.addItem("Visa")
            self.payType.addItem("American Express")
            self.payType.addItem("Mastercard")
            self.payType.addItem("JCB")
            self.payType.addItem("代金引換") #NOTE dont load card details

    #There are 3 different shipping regions: some of them have slightly different layouts
    #You can view the web pages in the shipping regions in the Data folder
    def changeRegion(self, string):
        if string == "us":
            self.add2.setEnabled(True)
            self.add3.setEnabled(True)
            self.payType.setEnabled(False)
            self.populateCountry(string)
        elif string == "eu":
            self.add2.setEnabled(True)
            self.add3.setEnabled(True)
            self.payType.setEnabled(True)
            self.populatePType(string)
            self.populateCountry(string)
        elif string == "asia":
            self.add2.setEnabled(False)
            self.add3.setEnabled(False)
            self.populatePType(string)
            self.populateCountry(string)

    def populateTime(self):
        for x in range(0, 25):
            y = "0" + str(x) + ":00"
            if x > 9:
                y = str(x) + ":00"
            self.time.addItem(y)

    #start() function is called when the go button is pressed
    #any value with a "O" on the end stands for Output i.e. the final
    #output value which will be sent to Supreme
    def start(self):
        nameO = (self.nameBox.text())
        emailO = (self.emailBox.text())
        phoneO = (self.phoneBox.text())
        addr1O = (self.add1.text())
        addr2O = (self.add2.text())
        addr3O = (self.add3.text())
        cityO = (self.city.text())
        zipO = (self.zip.text())
        cardnoO = self.cardno.text()
        cvvO = self.cvv.text()
        keywordsO = self.keywords.text()
        colourO = self.colour.text()

        #ATM there is a problem with receiving the data from the QListWidget
        #when the user changes a item within, it will not update till the widget
        #has been clicked so obviously this is not ideal
        #Thus, country, payment type, expiroy month and year are not working

        #    I      My attempt at receiving the value of country
        #    I
        #    V
        try:
            print(self.country.currentItem().text())
        except AttributeError:
            print(self.countryO)

        #Missing Attributes:
        #countryO, paymentTypeO, monthO, yearO, categoryO, timeO
        #regionO is also missing
    
    def orderArea(self):
        QLabel("Category", self).setGeometry(470, 250, 130, 30)
        self.cat = QListWidget(self)
        self.cat.setGeometry(470, 270, 130, 20)

        for x in range(0, len(categoryList)):
            self.cat.addItem(categoryList[x])

        QLabel("Keywords", self).setGeometry(470, 280, 100, 50)
        self.keywords = QLineEdit(self)
        self.keywords.setGeometry(470, 310, 150, 20)

        QCheckBox(self).setGeometry(470, 310, 50, 50)
        QLabel("Use Strict Item Search?", self).setGeometry(490, 310, 130, 50)

        QLabel("Colour", self).setGeometry(470, 340, 100, 50)
        self.colour = QLineEdit(self)
        self.colour.setGeometry(470, 370, 150, 20)

        QLabel("Domestic Time of Drop", self).setGeometry(470, 390, 130, 30)
        self.time = QListWidget(self)
        self.time.setGeometry(470, 410, 130, 20)
        self.populateTime()

        go = QPushButton(self)
        go.setGeometry(470, 450, 40, 30)
        go.setText("Go!")
        go.clicked.connect(lambda:self.start())
        
    def shipArea(self):
        QLabel("Choose Shipping Region", self).setGeometry(20, 250, 130, 30)
        self.eu = QRadioButton("EU", self)
        self.eu.setGeometry(20, 270, 50, 50)

        self.us = QRadioButton("US", self)
        self.us.setGeometry(60, 270, 50, 50)

        self.asia = QRadioButton("Asia", self)
        self.asia.setGeometry(100, 270, 50, 50)

        QLabel("Name", self).setGeometry(20, 300, 100, 50)
        self.nameBox = QLineEdit(self)
        self.nameBox.setGeometry(20, 330, 100, 20)

        QLabel("Email", self).setGeometry(20, 340, 100, 50)
        self.emailBox = QLineEdit(self)
        self.emailBox.setGeometry(20, 370, 100, 20)

        QLabel("Tel.", self).setGeometry(20, 380, 100, 50)
        self.phoneBox = QLineEdit(self)
        self.phoneBox.setGeometry(20, 410, 100, 20)

        QLabel("Add1", self).setGeometry(160, 260, 130, 30)
        self.add1 = QLineEdit(self)
        self.add1.setGeometry(160, 280, 100, 20)

        QLabel("Add2/APT(US)", self).setGeometry(160, 290, 100, 50)
        self.add2 = QLineEdit(self)
        self.add2.setGeometry(160, 320, 100, 20)

        QLabel("Add3/State(US)", self).setGeometry(160, 330, 100, 50)
        self.add3 = QLineEdit(self)
        self.add3.setGeometry(160, 360, 100, 20)

        QLabel("City", self).setGeometry(160, 370, 100, 50)
        self.city = QLineEdit(self)
        self.city.setGeometry(160, 400, 100, 20)

        QLabel("Post Code", self).setGeometry(160, 410, 100, 50)
        self.zip = QLineEdit(self)
        self.zip.setGeometry(160, 440, 100, 20)

        QLabel("Country/Province(ASIA)", self).setGeometry(300, 260, 130, 30)
        self.country = QListWidget(self)
        self.country.setGeometry(300, 280, 100, 20)

        QLabel("Payment Type", self).setGeometry(300, 300, 130, 30)
        self.payType = QListWidget(self)
        self.payType.setGeometry(300, 320, 130, 20)

        QLabel("Card No.", self).setGeometry(300, 330, 100, 50)
        self.cardno = QLineEdit(self)
        self.cardno.setGeometry(300, 360, 100, 20)

        QLabel("CVV", self).setGeometry(300, 370, 100, 50)
        self.cvv = QLineEdit(self)
        self.cvv.setGeometry(300, 400, 100, 20)


        QLabel("Expiry", self).setGeometry(300, 418, 130, 30)
        self.month = QListWidget(self)
        self.month.setGeometry(300, 440, 60, 20)
        self.year = QListWidget(self)
        self.year.setGeometry(370, 440, 60, 20)

        self.populateMonths()
        self.populateYears()
        
        self.eu.clicked.connect(lambda:self.changeRegion("eu"))
        self.us.clicked.connect(lambda:self.changeRegion("us"))
        self.asia.clicked.connect(lambda:self.changeRegion("asia"))
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def centre(self, width, height):
        self.move(width / 2 - (self.width / 2), height / 2 - (self.height / 2))


    #this function will set the current qlistitem to the flag
    #which is the saved data in this case
    def selectQList(self, flag, qlist):
        for x in range(0, len(qlist)):
            selected = qlist.item(x).text()
            if selected == flag:
                qlist.setCurrentRow(x)
                return flag    

    #this function works pretty well, to test it comment out window.startWindow in main
    #then create a new save and then run the program as the old saves may not work as well
            
    def populateFromSave(self, area):
        if area == "EU":
            self.changeRegion("eu")
            self.eu.setChecked(True)
            
            self.nameBox.setText((paydetails["Name"]))
            self.emailBox.setText((paydetails["Email"]))
            self.phoneBox.setText((paydetails["Phone"]))
            self.add1.setText((paydetails["Addr1"]))
            self.add2.setText((paydetails["Addr2"]))
            self.add3.setText((paydetails["Addr3"]))
            self.city.setText((paydetails["City"]))
            self.zip.setText((paydetails["Post/zip code"]))
            self.countryO = self.selectQList(paydetails["Country"], self.country)
            self.payTypeO = self.selectQList(paydetails["CardType"], self.payType)            
            self.cardno.setText((paydetails["Cardno"]))
            self.cvv.setText((paydetails["CardCVV"]))
            self.monthO = self.selectQList(paydetails["CardMonth"], self.month)
            self.yearO = self.selectQList(paydetails["CardYear"], self.year)
        elif area == "US":
            self.changeRegion("us")
            self.us.setChecked(True)

            self.nameBox.setText((paydetails["Name"]))
            self.emailBox.setText((paydetails["Email"]))
            self.phoneBox.setText((paydetails["Phone"]))
            self.add1.setText((paydetails["Addr1"]))
            self.add2.setText((paydetails["Addr2"]))#apt
            self.add3.setText((paydetails["Addr3"]))#state
            self.city.setText((paydetails["City"]))
            self.zip.setText((paydetails["Post/zip code"]))
            self.countryO = self.selectQList(paydetails["Country"], self.country)            
            self.cardno.setText((paydetails["Cardno"]))
            self.cvv.setText((paydetails["CardCVV"]))
            self.selectQList(paydetails["CardMonth"], self.month)
            self.selectQList(paydetails["CardYear"], self.year)
            
        elif area == "ASIA":
            self.changeRegion("asia")
            self.asia.setChecked(True)
            #CANNOT USE ASIAN PROFILE YET BECAUSE OF JAPANESE CHARACTERS


    #this works
    def passwordEntered(self, password):
        if not self.enterPass.isEnabled() == False:
           enc.password = password.encode('ascii')
           for x in paydetails:
                paydetails[x] = enc.readConf(x)
        self.populateFromSave(paydetails["Region"])


    def createNew(self):
        self.new.setParent(None)
        self.enterPass.setText("")
        self.enterPass.setEnabled(False)
        self.label.setText("Enter a password to save details")



    #function to save details - not working atm
    def saveDetails(self, password):
        global pDescr
        region = ""

        enc.paydetails = paydetails
        enc.initConf()

        paydetails["Name"] = (self.nameBox.text())
        paydetails["Email"] = (self.emailBox.text())
        paydetails["Phone"] = (self.phoneBox.text())
        paydetails["Addr1"] = (self.add1.text())
        paydetails["Addr2"] = (self.add2.text())
        paydetails["Addr3"] = (self.add3.text())
        paydetails["City"] = (self.city.text())
        paydetails["Post/zip code"] = (self.zip.text())
        paydetails["Country"] = (self.country.currentItem())
        paydetails["CardType"] = (self.payType.currentItem())
        paydetails["Cardno"] = (self.cardno.text())
        paydetails["CardCVV"] = (self.cvv.text())
        paydetails["CardMonth"] = (self.month.currentItem())
        paydetails["CardYear"] = (self.year.currentItem())
        paydetails["Region"] = (region)

        #this bit is giving me trouble I think the formatting of paydetails is wrong
        enc.password = password.encode('ascii')
        for x in paydetails:
            enc.writeToConf(x, paydetails[x])


    #creates the file support area below the logo
    def passwordCheck(self, isPasswordExists):
        if isPasswordExists:
            detected_profile = "Profile detected, enter password to use"
            self.label = QLabel(detected_profile, self)
            self.label.setGeometry(10, 170, 300, 20)
            
            self.enterPass = QLineEdit(self)
            self.enterPass.name = "enterPass"
            self.enterPass.setGeometry(10, 190, 200, 20)

            confirm = QPushButton(self)
            confirm.setObjectName = "confirm"
            confirm.setGeometry(220, 190, 40, 30)
            confirm.setEnabled(False)
            confirm.setText("Enter")

            self.new = QPushButton(self)
            self.new.setObjectName = "new"
            self.new.setGeometry(270, 190, 40, 30)
            self.new.setText("New")
            self.new.setCheckable(True)

            self.enterPass.textChanged.connect(lambda:confirm.setEnabled(True))

            confirm.clicked.connect(lambda:self.passwordEntered(self.enterPass.text()))
            self.new.clicked.connect(lambda:self.createNew())#this bit should trigger the code in the else
        else:
            detected_profile = "No profile detected, enter details below and create a password to save details!"
            self.label = QLabel(detected_profile, self)
            self.label.setGeometry(10, 170, 400, 20)
            
            self.enterNewPass = QLineEdit(self)
            self.enterNewPass.setGeometry(10, 190, 200, 20)

            save = QPushButton(self)
            save.setGeometry(220, 190, 40, 30)
            save.setEnabled(True)
            save.setText("Save")
            save.clicked.connect(lambda:self.saveDetails("123"))

#creates a new window and starts it
def startWindow(isPasswordExists):
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    
    ex = App(isPasswordExists)
    ex.centre(size.width(), size.height())
    sys.exit(app.exec_())

