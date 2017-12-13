def selectName():
    name = input("Enter Name: ")
    return name

def selectEmail():
    email = input("Enter Email: ")
    return email

def selectPhone():
    phone = input("Enter Phone Number: ")
    return phone

def selectAdd1():
    add1 = input("Enter Address 1: ")
    return add1

def selectAdd2():
    add2 = input("Enter Address 2: ")
    return add2

def selectAdd3():
    add3 = input("Enter Address 3: ")
    return add3

def selectCity():
    city = input("Enter City: ")
    return city

def selectPostcode():
    postcode = input("Enter Postcode: ")
    return postcode

def selectCardno():
    cardno = input("Enter Card Number: ")
    return cardno

def selectCardx():
    cardX = input("Enter Card CVV: ")
    return cardX

def selectCardx1():
    cardX1 = input("Enter Card Month Expire Date (e.g. 05 for may): ")
    return cardX1

def selectCardx2():
    cardX2 = input("Enter Card Month Expire Year: ")
    return cardX2

def selectCardType():
    cardX2 = input("Enter Payment Type (e.g. Solo, Visa, PayPal): ")
    if cardX2 == "PayPal":
        cardType1 = 1
    return cardX2

def m():
    selectName()
    selectEmail()
    selectPhone()
    selectAdd1()
    selectAdd2()
    selectAdd3()
    selectCity()
    selectPostcode()
    selectCardno()
    selectCardx()
    selectCardx1()
    selectCardx2()
    selectCardType()
