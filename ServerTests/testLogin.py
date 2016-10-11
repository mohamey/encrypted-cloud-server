import requests

print("Trying log in now")

payload = {
    "RequestType" : "LOGIN",
    "name" : "root",
    "password" : "admin"
}

res = requests.post("http://mohamey.me/login.php", data=payload)
print(res.text)
