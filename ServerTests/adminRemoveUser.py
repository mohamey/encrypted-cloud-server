import requests

payload = {
    "RequestType" : "REMOVE",
    "name" : "root",
    "password" : "admin",
    "removalName" : "yasir"
}

res = requests.post("http://mohamey.me/login.php", data=payload)

print(res.text)
