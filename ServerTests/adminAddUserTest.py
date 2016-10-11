import requests

payload = {
    "RequestType" : "CREATE",
    "name" : "root",
    "password" : "admin",
    "newName" : "yasir",
    "newPass" : "Legend",
    "admin" : "no"
}

res = requests.post("http://mohamey.me/login.php", data=payload)

print(res.text)
