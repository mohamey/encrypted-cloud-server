import requests

payload = {
    "RequestType" : "CREATE",
    "name" : "yasir",
    "password" : "temp",
    "newName" : "root",
    "newPass" : "admin",
    "admin" : "yes"
}

res = requests.post("http://mohamey.me/login.php", data=payload)
print(res.text)
