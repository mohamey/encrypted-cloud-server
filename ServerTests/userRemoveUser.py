import requests

payload = {
    "RequestType" : "REMOVE",
    "name" : "yasir",
    "password" : "Legend",
    "removalName" : "murph"
}

res = requests.post("http://mohamey.me/login.php", data=payload)

print(res.text)
