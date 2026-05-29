import sqlite3 # The library that allows me to directly execute lines of sql and add passwords to the database
import ctypes # This allows for me to use memset and a few other functions to overwrite buffers and release memory
import sys # Allows me to keep the python script running until the application gets closed
import base64 # For encoding into the proper key formatting for the fernet encryption algorithm
import app # What will eventually be the main app file that holds my Qt GUI
from pathlib import Path
from PySide6 import QtWidgets # Lets me add the QApplication to keep track of the application's state/alive or dead
from cryptography.fernet import Fernet # For creating encryption/decryption key for encrypting the data inside of the database
from HashingUtils import keyDerivation, verifyPW # My file that implements the key generation and possibly the encryption of data

thisApp = QtWidgets.QApplication()

myApp = app.Stacks()

with open('./Style/app.qss', 'r') as f:
    myApp.setStyleSheet(f.read())

myApp.resize(800, 600)
myApp.show()

sys.exit(thisApp.exec())