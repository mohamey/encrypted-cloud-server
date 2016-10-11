import requests

payload = {
    "RequestType" : "CREATE",
    "name" : "yasir",
    "password" : "Legend",
    "newName" : "murphc",
    "newPass" : "n00b",
    "admin" : "no"
}

res = requests.post("http://mohamey.me/login.php", data=payload)

print(res.text)
