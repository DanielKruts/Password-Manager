#|------------------------------------------------------------------------------------------------------------------|#
#| This file contains the class that I will create for my app. I am simply separating it from the                   |#
#| passwordManager.py file so that there is more organization being introduced into the development of this app     |#
#| Author: Daniel Krutsick                                                                                          |#
#|------------------------------------------------------------------------------------------------------------------|#
from PySide6 import QtCore, QtWidgets, QtGui # For creating a GUI

#|------------------------------------------------------------------------------------------------------------------|#
#| Helpful reminder of some of the imports from different Qt library additions                                      |#
#| QtWidgets:                                                                                                       |#
#|      QLabel: Lets you edit labels and apply styling to them.                                                     |#
#|      Check the website for more about the different Widget options                                               |#
#| QtCore:                                                                                                          |#
#|      All of the different options for the styling                                                                |#
#|------------------------------------------------------------------------------------------------------------------|#

class NewPasswordPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pw = QtWidgets.QInputDialog()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pw)

#|---------------------------------------|#
#| Page for logging in, self explanatory |#
#|---------------------------------------|#
class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.pw = QtWidgets.QLineEdit()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.pw)

#|----------------------------------------|#
#| Page for the vault, or after you login |#
#|----------------------------------------|#
class VaultPage(QtWidgets.QWidget):
    logoutSuccess = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.passwordButton = QtWidgets.QPushButton("Push to see your passwords")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.passwordButton)

        self.passwordButton.clicked.connect(self.logout)

    def logout(self):
        self.logoutSuccess.emit()


        
#|----------------------------------------|#
#| The class maintaining the three pages  |#
#|----------------------------------------|#
class Stacks(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #-- Initialization of the stacked widget                    --#
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        #-- Initializing each individual page for the stack         --#
        self.loginPage = LoginPage()
        self.vaultPage = VaultPage()
        self.pwPage = NewPasswordPage()

        #-- Adding all of the widgets onto the stack                --#
        self.stack.addWidget(self.loginPage)
        self.stack.addWidget(self.vaultPage)
        self.stack.addWidget(self.pwPage)

        #-- Where the currentIndex is set at by default(Login Page) --#
        self.stack.setCurrentIndex(0)

        #-- All of the receivers for the signals sent by the pages  --#
        self.vaultPage.logoutSuccess.connect(self.logout)

    def logout(self):
        self.stack.setCurrentIndex(0)