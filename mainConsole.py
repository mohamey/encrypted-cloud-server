import webbrowser
from tkinter import *
from tkinter import messagebox
import addNewUser as newUserDialog
import removeUser as removeUserDialog
import login
import cipherFunctions as cipher
import config
import requests

#Process the decrypt file inputs
def processDecryptButton(location, name, key, frame):
    if ((location=="") or (name=="Browse...") or (key=="")):
        messagebox.showwarning("Error", "Error parsing inputs while decrypting file")
        return
    #When inputs are okay, try decrypting the file
    if cipher.decryptFile(location, name, key):
        messagebox.showinfo("Success!", "The file was successfully decrypted. Please find it in the Decrypted Files folder")
        login.destroyGrid(frame)
        generateMainWindow(frame)
    else:
        messagebox.showerror("Unsuccessful", "There was a problem decrypting the specified file")

#Process the encrypt file inputs
def processEncryptButton(location, name, key, frame):
    if ((location=="") or (name=="Browse...") or (key=="")):
        messagebox.showerror("Error", "Error occured while parsing inputs to encrypt file")
        return
    #When inputs are okay, try decrypting file
    if cipher.encryptFile(location, name, key):
        messagebox.showinfo("Success!", "The File was successfully encrypted. Please find it in the Encrypted Files Folder")
        login.destroyGrid(frame)
        generateMainWindow(frame)
    else:
        messagebox.showerror("Unsuccessful", "There was a problem encrypting the specified file")

def processAddUserFrame(frame):
    login.destroyGrid(frame)
    newUserDialog.generateAddUserFrame(frame)

def processRemoveUserFrame(frame):
    login.destroyGrid(frame)
    removeUserDialog.generateRemoveUserFrame(frame)

def getFileNames():
    name = config.getName()
    password = config.getPassword()
    payload = {
        "name" : name,
        "password" : password,
        "RequestType" : "listDirectory"
    }
    res = requests.post("http://mohamey.me/login.php", data=payload)
    files = ((res.text)[5:]).split(",")
    return files

def downloadFile(filename):
    if filename == "Select File":
        messagebox.showerror("Error", "You must select a file from the dropdown")
        return
    payload = {"file":filename}
    res = requests.get("http://mohamey.me/login.php", params=payload)
    fileObject = open("Downloads/"+filename, 'wb')
    fileObject.write(res.content)
    fileObject.close()
    messagebox.showinfo("Success", "Download Complete, please find the file in the downloads folder where you will need to decrypt it")

def uploadFile(fileLocation, frame):
    fileUpload = {"file" : open(fileLocation, 'rb')}
    payload = {
        "RequestType" : "uploadFile",
        "name" : config.getName(),
        "password" : config.getPassword()
    }
    res = requests.post("http://mohamey.me/login.php", data = payload, files=fileUpload)
    if res.text == "Successfully uploaded file":
        messagebox.showinfo("Result", res.text)
        destroyGrid(frame)
        generateMainWindow(frame)
    else:
        messagebox.showerror("Error", res.text)

def generateMainWindow(frame):
    frame.wm_title("User Console")
    global USERNAME
    global PASSWORD

    #Open file browser dialog
    def browseFile(fileVar, fileLocationVar):
        from tkinter import filedialog
        fileLocation = filedialog.askopenfilename(filetypes=[("Any", "*.*")])
        if len(fileLocation) > 0:
            displayName = str(fileLocation).split('/')
            fileVar.set(displayName[-1])
            fileLocationVar.set(fileLocation)
        return

    #Download File row
    downloadOption = StringVar()
    downloadOption.set("Select File")
    serverFiles = getFileNames()
    downloadFileLabel = Label(text="Download File")
    downloadFileLabel.grid(row=0, column=0, sticky="W")
    dropDown = OptionMenu(frame, downloadOption, *serverFiles)
    dropDown.grid(row=0, column=1, padx=5, pady=5)
    downloadButton = Button(text="Download File", command = lambda: downloadFile(downloadOption.get()))
    downloadButton.grid(row=0, column=2, padx=5, pady=5)

    #Upload File row
    uploadOption = StringVar()
    uploadOption.set("Browse...")
    uploadFileLocation = StringVar()
    uploadFileLocation.set("Browse...")

    uploadFileLabel = Label(text="Upload File")
    uploadFileLabel.grid(row=1, column=0, sticky="W")
    uploadBrowseButton = Button(textvar=uploadOption, command=lambda: (browseFile(uploadOption, uploadFileLocation)))
    uploadBrowseButton.grid(row=1, column=1, padx=5, pady=5)

    uploadButton = Button(text="Upload File", command=lambda:(uploadFile(uploadFileLocation.get(), frame)))
    uploadButton.grid(row=1, column=2, padx=5, pady=5)

    #Select the file you would like to decrypt | File browser | Decrypt
    decryptFileLocation = StringVar()
    decryptFileLocation.set("Browse...")
    decryptLabel = Label(text="Select the file you would like to decrypt")
    decryptLabel.grid(row=2, column=0, sticky="W")

    decryptFileVar = StringVar()
    decryptFileVar.set("Browse...")
    decryptBrowseButton = Button(textvar=decryptFileVar, command= lambda:(browseFile(decryptFileVar, decryptFileLocation)))
    decryptBrowseButton.grid(row=2, column=1, padx=5, pady=5)

    decryptButton = Button(text="Decrypt File", command= lambda:(processDecryptButton(decryptFileLocation.get(), decryptFileVar.get(), config.getKey(), frame)))
    decryptButton.grid(row=2, column=2, padx=5, pady=5)

    #Select the file you would like to Encrypt | File Browser | Encrypt
    encryptFileLocation = StringVar()
    encryptFileLocation.set("")
    encryptLabel = Label(text="Select the File you would like to Encrypt")
    encryptLabel.grid(row=3, column=0, sticky="W")

    encryptFileVar = StringVar()
    encryptFileVar.set("Browse...")
    encryptBrowseButton = Button(textvar=encryptFileVar, command=lambda:(browseFile(encryptFileVar, encryptFileLocation)))
    encryptBrowseButton.grid(row=3, column=1, padx=5, pady=5)

    encryptButton = Button(text="Encrypt File", command= lambda: (processEncryptButton(encryptFileLocation.get(), encryptFileVar.get(), config.getKey(), frame)))
    encryptButton.grid(row=3, column=2, padx=5, pady=5)

    #Show buttons for user addition and removal
    addUserButton = Button(text="Add New User", command= lambda: processAddUserFrame(frame))
    addUserButton.grid(row=4, column=1, padx=5, pady=5)

    removeUserButton = Button(text="Remove Existing User", command= lambda: (processRemoveUserFrame(frame)))
    removeUserButton.grid(row=4, column=2, padx=5, pady=5)
