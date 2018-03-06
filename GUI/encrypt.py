import os.path
from configparser import ConfigParser
from collections import OrderedDict
from hashlib import sha256
import aes
from base64 import b64encode, b64decode
import functions as func

def checkIfStore():
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
            func.useConfig = True
            func.password = password
        else:
            useConfig = False

def decr(value, password):
    m = sha256()
    m.update(password)
    passwd = m.digest()
    iv = m.digest()[::2]
    cipher = aes.AESModeOfOperationCFB(passwd, iv = iv)
    decrypted = cipher.decrypt(b64decode(value))
    return decrypted[:-ord(decrypted[-1:])].decode('ascii')

def encr(value, password):
    m = sha256()
    m.update(password)
    key = m.digest()
    iv = m.digest()[::2]
    pad = 16 - len(value) % 16
    raw = value + pad * chr(pad)
    cipher = aes.AESModeOfOperationCFB(key, iv = iv)
    return b64encode(cipher.encrypt(raw)).decode('ascii')

def readConf(key, password):
    config = ConfigParser()
    config.read('config.cnf')
    try:
        return decr(config.get(config.sections()[0], key), password)
    except TypeError:
        return ''

def writeToConf(key, value, password):
    config = ConfigParser()
    config.read('config.cnf')
    encValue = encr(value, password)
    config.set(config.sections()[0], key, encValue)
    cfgfile = open('config.cnf', 'w')
    config.write(cfgfile)
    cfgfile.close()
