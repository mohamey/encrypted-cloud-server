import requests

payload = {
    "name" : "root",
    "password" : "admin",
    "RequestType" : "listDirectory"
}

res = requests.post("http://mohamey.me/login.php", data=payload)
print(res.text)
