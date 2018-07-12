from configparser import ConfigParser
from hashlib import sha256
from base64 import b64encode, b64decode
from collections import OrderedDict
import aes

paydetails = OrderedDict(
    [('Name', ''), ('Email', ''), ('Phone', ''), ('Addr1', ''), ('Addr2', ''), ('Addr3', ''),
     ('City', ''), ('Post/zip code', ''), ('Country', ''), ('CardType', ''), ('Cardno', ''),
     ('CardCVV', ''), ('CardMonth', ''), ('CardYear', '')])

def decr(value):
    m = sha256()
    m.update(password)
    passwd = m.digest()
    iv = m.digest()[::2]
    cipher = aes.AESModeOfOperationCFB(passwd, iv = iv)
    decrypted = cipher.decrypt(b64decode(value))
    try:
        return decrypted[:-ord(decrypted[-1:])].decode('utf-8')
    except UnicodeDecodeError:
        print('Password is probably incorrect')
        exit(1)

def readConf(key, f):
    config = ConfigParser()
    config.read(f)
    try:
        return decr(config.get(config.sections()[0], key))
    except TypeError:
        print('Password is probably incorrect')
        exit(1)


password = input('pass: ').encode('utf-8')
file = input('file: ')

for x in paydetails:
    print(x, readConf(x, file))
