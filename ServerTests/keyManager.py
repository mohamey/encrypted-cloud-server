import random
import requests
import config

#Generate a random key to be used in file encryption/decryption
def keyGen():
	availableChars=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	availableChars.extend(['1','2','3','4','5','6','7','8','9','0'])
	availableChars.extend([',','.','!','"','£','$','%','^','&','*','(',')','-','_','=','+'])
	result = ""
	for i in range(1..40):
		index = random.randrange(0,len(availableChars)-1)
		result = result+availableChars[index]
	return result

def updateKey(key):

