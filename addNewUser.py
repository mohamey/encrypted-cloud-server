import requests
import config
import login
import mainConsole
from tkinter import messagebox
from tkinter import *

# Send the new user information to the remote database
def processAddition(name, password, passwordConfirmation, admin, frame):
    if not config.getAdmin():
        messagebox.showerror("Unauthorized", "You have insufficient permissions to carry out this action")
        return;
    elif (len(name) == 0) or (len(password) == 0) or (len(admin)==0):
        messagebox.showerror("Error", "You cannot leave any fields blank")
        return
    elif (password != passwordConfirmation) or len(password) == 0:
        messagebox.showerror("Error", "The password confirmation does not match the password. Please try again")
        return
    payload = {
        "RequestType" : "CREATE",
        "name" : config.getName(),
        "password" : config.getPassword(),
        "newName" : name,
        "newPass" : password,
        "admin" : admin
    }

    res = requests.post("http://mohamey.me/login.php", data=payload)
    if res.text == "Successfully created new user":
        messagebox.showinfo("Success", res.text)
        login.destroyGrid(frame)
        generateAddUserFrame(frame)
    else:
        messagebox.showwarning("Result", res.text)
    return

# Return to the main user interface
def returnToMain(frame):
    login.destroyGrid(frame)
    mainConsole.generateMainWindow(frame)

# Generate the UI for adding a new user
def generateAddUserFrame(frame):
    #Label to enter new userName
    newNameLabel = Label(text="New Username")
    newNameLabel.grid(row=0, column=0, sticky="W")

    #Add name entry area
    newName = Entry(frame)
    newName.grid(row=0, column=1,padx=5, pady=5)

    #Label to enter password
    pWordLabel = Label(text="New Password")
    pWordLabel.grid(row=1, column=0, sticky="W")

    #Entry for password
    pWord = Entry(frame, show="*")
    pWord.grid(row=1, column=1, padx=5, pady=5)

    #Label to confirm password
    pWordConfLabel = Label(text="Confirm Password")
    pWordConfLabel.grid(row=2, column=0,sticky="W")

    #Entry for password Confirmation
    pWordConf = Entry(frame, show="*")
    pWordConf.grid(row=2,column=1,padx=5,pady=5)

    #Give new user admin privileges
    adminPrivs = StringVar()
    adminPrivs.set("no")
    giveAdmin = Checkbutton(text="Give Admin Privileges",variable=adminPrivs, onvalue="yes", offvalue="no")
    giveAdmin.grid(row=3, column=0, columnspan=2, pady=5)

    #Cancel adding new user
    cancelButton = Button(text="Cancel", command=lambda: returnToMain(frame))
    cancelButton.grid(row=4, column=0, padx=5, pady=5)

    #Button to confirm adding user
    confirmAddButton = Button(text="Add User", command=lambda: processAddition(newName.get(), pWord.get(), pWordConf.get(), adminPrivs.get(), frame))
    confirmAddButton.grid(row=4,column=1,padx=5,pady=5)
