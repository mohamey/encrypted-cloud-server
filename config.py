import requests

#Store data to be used across Files
USERNAME = PASSWORD = KEY = ACCESS_TOKEN = ""
ADMIN = False

def updateLogin(name, pword):
    global USERNAME
    global PASSWORD
    USERNAME = name
    PASSWORD = pword

def updateKey(newKey):
    global KEY
    KEY = newKey

def updateAdmin(newBool):
    global ADMIN
    ADMIN = newBool

def getName():
    global USERNAME
    return USERNAME

def getPassword():
    global PASSWORD
    return PASSWORD

def getKey():
    global KEY
    return KEY

def getAdmin():
    global ADMIN
    return ADMIN

def getAuthenticationKey():
    global USERNAME
    global PASSWORD
    global KEY
    payload = {
        "name" : USERNAME,
        "password" : PASSWORD,
        "RequestType" : "getKey"
    }

    try:
        res = requests.post("http://mohamey.me/login.php", data=payload)
        KEY = res.text
    except Exception as e:
        print(e)
        return False
    return True
