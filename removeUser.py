import requests
import config
import login
import addNewUser
import mainConsole
from tkinter import messagebox
from tkinter import *

def processRemoveUser(name, password, frame):
    if len(name) == 0:
        messagebox.showerror("Error", "You cannot leave the name field blank")
        return
    elif config.getAdmin() == False:
        messagebox.showerror("Insufficient Permissions", "You do not have the authorization to carry out this request")
        return
    elif password != config.getPassword():
        messagebox.showerror("Incorrect Password", "Wrong password entered, could not verify user")
        return

    result = messagebox.askquestion("Remove User", "Are you sure you want to remove "+name+" from our super secret group?")
    if "no" == result:
        return

    payload = {
        "RequestType" : "REMOVE",
        "name" : config.getName(),
        "password" : config.getPassword(),
        "removalName" : name
    }
    res = requests.post("http://mohamey.me/login.php", data=payload)
    if res.text == "User successfully removed":
        messagebox.showinfo("Success", "User successfully removed")
        login.destroyGrid(frame)
        generateRemoveUserFrame(frame)
    else:
        messagebox.showwarning("Result", res.text)
    return

def generateRemoveUserFrame(frame):
    #Label to enter the name of the user to be removed
    nameLabel = Label(text="Enter the name of user to be removed")
    nameLabel.grid(row=0, column=0, sticky="W")

    #Add name entry area
    name = Entry(frame)
    name.grid(row=0, column=1, padx=5, pady=5)

    #Add password entry label
    passLabel = Label(text="Please confirm your password")
    passLabel.grid(row=1, column=0, sticky="W")

    #Add Password entry area
    password = Entry(show="*")
    password.grid(row=1, column=1, padx=5, pady=5)

    #Cancel Button to go out to main screen
    cancelButton = Button(text="Cancel", command= lambda: addNewUser.returnToMain(frame))
    cancelButton.grid(row=2, column=0, padx=5, pady=5)

    #Remove User Button
    removeButton = Button(text="Remove User", command= lambda: processRemoveUser(name.get(), password.get(), frame))
    removeButton.grid(row=2, column=1, padx=5, pady=5)
