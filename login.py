from tkinter import *
from tkinter import messagebox
import requests
import config
import mainConsole

#Destroy all the frames in a grid
def destroyGrid(frame):
    for widget in frame.grid_slaves():
        widget.destroy()

#Generate the login window presented upon starting the program
def generateLoginWindow(frame):
    #process the login details inputted by the user
    global USERNAME
    global PASSWORD
    def processLogin(uname, pword):
        payload = {
            "RequestType" : "LOGIN",
            "name" : uname,
            "password" : pword
        }
        res = requests.post("http://mohamey.me/login.php", data=payload)
        if res.text == "y" or res.text == "n":
            config.updateLogin(uname, pword)
            if res.text == "y":
                config.updateAdmin(True)
            config.getAuthenticationKey()
            messagebox.showinfo("Success!", "Login Successful")
            destroyGrid(frame)
            mainConsole.generateMainWindow(frame)
        else:
            messagebox.showerror('Login Failed', 'Please check your User name and password and try again')
    frame.wm_title("Super Secret File Encryption")
    #Variables used for logging in
    userName = passWord = ""
    #Create and place label for user name entry
    uNameLabel = Label(text="User Name")
    uNameLabel.grid(row=0, column=0, sticky="W")

    #Create and place entry for User Name
    uName = Entry(frame)
    uName.grid(row=0, column=1, padx=5, pady=5)

    #Create and place label for password entry
    pWordLabel = Label(text="Password")
    pWordLabel.grid(row=1, column=0, sticky="W")

    #Create and place entry for Password
    pWord = Entry(show="*")
    pWord.grid(row=1, column=1, padx=5, pady=5)

    #Create and place the login button
    loginButton = Button(text="Login", command= lambda: processLogin(uName.get(), pWord.get()))
    loginButton.grid(row=3, column=0, columnspan=2, pady=5)

if __name__ == '__main__':
    root = Tk()
    generateLoginWindow(root)
    root.mainloop()
