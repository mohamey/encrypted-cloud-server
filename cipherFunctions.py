from simplecrypt import encrypt, decrypt, DecryptionException
from tkinter import messagebox

def encryptFile(location, name, key):
    with open(location, "rb") as unencryptedFile:
        byteForm = unencryptedFile.read()
        encryptedBytes = encrypt(key, byteForm)
        try:
            destinationFile = "EncryptedFiles/"+name
            encryptedFile = open(destinationFile, "wb")
            encryptedFile.write(encryptedBytes)
            encryptedFile.close()
            return True
        except:
            print("An error occured writing the encrypted bytes to file")
    return False

def decryptFile(location, name, key):
    with open(location, "rb") as encryptedFile:
        try:
            encryptedBytes = encryptedFile.read()
            decryptedBytes = decrypt(key, encryptedBytes)
        except DecryptionException:
            messagebox.showwarning("Error","This file was not encrypted by this group")
            return
        except:
            return False
        try:
            decryptLocation = "DecryptedFiles/"+name
            decryptTarget = open(decryptLocation, "wb")
            decryptTarget.write(decryptedBytes)
            decryptTarget.close()
            return True
        except:
            print("Error writing to decrypted target file")
            return False
