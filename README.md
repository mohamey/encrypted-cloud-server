# Encrypted Cloud Storage
A private cloud server that used to be hosted on my [website](http://mohamey.me), on the clientside it's written in Python3, and on the server side it's in PHP and MySql. The server has a few PHP scripts that handle encrypting and decrypting files, and the database keeps records of the users and their salted-hashed passwords. Only an admin can add or remove users, and key management is handled by the server, it is securely transmitted to the client application, all files held on the server are encrypted using AES-256, and is only ever decrypted on the client machine.

## Requirements
* PHP5 Compatible Server
* MySql on Server
* Python3 on Client computer

## Set up
The files for the server are in a handy directory called `ServerSide`. `Login.php` should be placed somewhere accessible to the public so requests can be made. The file `usersTable.sql` should be used to create the necessary table to store login information, in the database `CS3041`.

## Usage
First you need to manually add an admin user to the database so you can actually login to the server, and create more users. Then to start the GUI simply run
```
python3 login.py
```
