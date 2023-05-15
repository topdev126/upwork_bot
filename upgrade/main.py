from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow
from threading import *
import json

from helper import *
from core import *

STATUS_IDLE = 0
STATUS_SIGNUP = 1
STATUS_LOGIN = 2
STATUS_BID = 3

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        fontId = QtGui.QFontDatabase.addApplicationFont('assets/fonts/BITCBLKAD.ttf')
        if fontId < 0:
            print('Not load font')
        
        uic.loadUi(resource_path("ui/main.ui"), self)

        self.setWindowTitle("For Upwork")
        self.setFixedSize(900, 500)

        self.canAutoBid = True

        self.info = None
        self.driver = None

        self.signupThread = None
        self.loginThread = None
        self.autoBidThread = None

        self.setStatus(STATUS_IDLE)
        
        self.initUI() 

        self.autoBidAfterSignup = self.autoSignupCheckBox.isChecked()
        self.autoBidAfterLogin = self.autoLoginCheckBox.isChecked()
        self.sendMsgToTelegram = self.sendMsgToTelegramCheckBox.isChecked()

        try:
            self.info = self.getConfigInfo()
        except Exception as e:
            print(e)
            self.printMessage('Something went wrong while getting setting information from config file.')
        
        self.printAccountInformation()
            
    def initUI(self):
        self.signupButton.clicked.connect(self.signupProcess)
        self.loginButton.clicked.connect(self.loginProcess)
        self.autoButton.clicked.connect(self.autoBidProcess)

        self.autoButton.setEnabled(False)

        self.signupTimesEdit.setText(str(SIGNUP_TIMES))
        self.signupIntervalTimeEdit.setText(str(SIGNUP_INTERVAL_TIME))
        self.autoBidIntervalTimeEdit.setText(str(AUTOBID_INTERVAL_TIME))

    def getConfigInfo(self):
        with open(CONFIG_FILE_NAME, "r") as f:
            return json.load(f)

    def printAccountInformation(self):
        self.nameEdit.setText(self.info['firstName'] + ' ' + self.info['lastName'])
        self.countryEdit.setText(self.info['country'])

    def printMessage(self, message):
        self.statusLabel.setText(message)

    def writeEmailLog(self, email):
        with open(EMAIL_CHECK_FILE, 'a') as f:
            f.write(f"{email}\n")  

    def setStatus(self, status):
        self.status = status
        if status is STATUS_IDLE:
            self.signupButton.setText('Sign up')
            self.signupButton.setEnabled(True)
            self.loginButton.setText('Log in')
            self.loginButton.setEnabled(True)
            self.autoButton.setText('Auto-bid')
            if self.canAutoBid and self.driver is not None: self.autoButton.setEnabled(True)
        elif status is STATUS_SIGNUP:
            self.signupButton.setText('Signing up')

            self.signupButton.setEnabled(False)
            self.loginButton.setEnabled(False)
            self.autoButton.setEnabled(False)

            self.canAutoBid = False
        elif status is STATUS_LOGIN:
            self.loginButton.setText('Logging in')
            self.signupButton.setEnabled(False)
            self.loginButton.setEnabled(False)
            self.autoButton.setEnabled(False)

            self.canAutoBid = False
        elif status is STATUS_BID:
            self.canAutoBid = False
            self.autoButton.setText('Stop bid')

    def signupProcess(self):
        if self.status is not STATUS_IDLE: return
        if self.signupThread is not None:
            self.signupThread = None

        self.signupThread = Thread(target = self.handleSignup)
        self.signupThread.start()
    
    def loginProcess(self):
        if self.status is not STATUS_IDLE: return
        if self.loginThread is not None:
            self.loginThread = None

        self.loginThread = Thread(target = self.handleLogin)
        self.loginThread.start()

    def autoBidProcess(self):
        if self.autoBidThread is not None:
            self.autoBidThread = None
            self.setStatus(STATUS_IDLE)
        else:
            self.autoBidThread = Thread(target = self.autoBid)
            self.autoBidThread.start()

    def handleSignup(self):
        self.autoBidAfterSignup = self.autoSignupCheckBox.isChecked()

        if self.autoBidAfterSignup:
            signUPTimes = self.signupTimesEdit.text()
            try:
                signupTimes = int(signUPTimes)
            except: 
                signUPTimes = 1
                pass

            signupIntervalTime = self.signupIntervalTimeEdit.text()
            try:
                signupIntervalTime = int(signupIntervalTime)
            except: 
                signupIntervalTime = SIGNUP_INTERVAL_TIME
                pass

            self.canAutoBid = False
            n = 0
            success = True
            while(success and n < signupTimes):
                if self.driver is not None:
                    self.driver.quit()
                self.driver = getChromeDriver()

                self.setStatus(STATUS_SIGNUP)
                success = self.signup()
                self.setStatus(STATUS_IDLE)
                if success:
                    self.setStatus(STATUS_BID)
                    success = self.autoBid()
                    self.setStatus(STATUS_IDLE)

                    # Delay
                    self.printMessage('Idling ...')
                    time.sleep(signupIntervalTime * 60)
                else: self.printMessage('Error while in signing up')
                n += 1
            self.printMessage('Completed!')
        else:
            if self.driver is None:
                self.driver = getChromeDriver()
            self.setStatus(STATUS_SIGNUP)
            success = self.signup()
            if success:
                self.canAutoBid = True
                self.printMessage('Completed!')
            else: 
                self.canAutoBid = False
                self.printMessage('Error while signing up')
            self.setStatus(STATUS_IDLE)
    
    def handleLogin(self):
        email = self.emailEdit.text()
        if email.strip() == '':
            self.printMessage('Please input email address to log in')
            return

        self.autoBidAfterLogin = self.autoLoginCheckBox.isChecked()
        if self.driver is None:
            self.driver = getChromeDriver()
        if self.autoBidAfterLogin:
            self.canAutoBid = False
            self.setStatus(STATUS_LOGIN)
            success = self.login()
            if success:
                self.setStatus(STATUS_BID)
                if success: 
                    self.autoBid()
                    self.printMessage('Completed!')
            else: self.printMessage('Error while logging in')
            self.setStatus(STATUS_IDLE)
        else:
            self.setStatus(STATUS_LOGIN)
            success = self.login()
            if success: 
                self.canAutoBid = True
                self.printMessage('Completed!')
            else:
                self.canAutoBid = False
                self.printMessage('Error while logging in')
            self.setStatus(STATUS_IDLE)

    def handleAutobid(self):
        if self.canAutoBid and self.driver is not None: 
            self.setStatus(STATUS_BID)
            success = self.autoBid()
            if success: self.printMessage('Completed!')
            else: self.printMessage('Error while auto bidding')
            self.setStatus(STATUS_IDLE)
        else: self.printMessage('Please log in')

        self.printMessage('Completed!')

    def autoBid(self):
        self.printMessage("Automatically bidding ... ")
        autoBidIntervalTime = self.autoBidIntervalTimeEdit.text()
        try:
            autoBidIntervalTime = int(autoBidIntervalTime)
        except: 
            autoBidIntervalTime = AUTOBID_INTERVAL_TIME
            pass
        try:
            self.setStatus(STATUS_BID)
            result = Core.autoBid(autoBidIntervalTime, self.info, self.driver)
            self.setStatus(STATUS_IDLE)
            if result == INSUFFICIENT_CONNECTS:
                self.printMessage("Insufficient connect balances.")
            elif result == 130:
                self.printMessage("Unexpected Error in auto bid ... ")
            else: 
                self.printMessage("Something went wrong")
            
            if result == INSUFFICIENT_CONNECTS: return True
            return False
        except: 
            self.printMessage("Unexpected Error in auto bid ... ")
            return False

    def signup(self):
        try:
            emailAddress = generateFakeEmail(self.info['gmailUser'], self.info['emailSuffixCount'])
            self.emailEdit.setText(emailAddress)
            self.printMessage("Please wait while signing up ... ")

            result = Core.signUp(emailAddress, self.info, self.driver)
            if result:
                self.printMessage("Verifying email...")

                emailVerificationUrl = getUpworkVerifyLink(emailAddress, self.info['gmailUser'], self.info['gmailPassword'])
                if emailVerificationUrl:
                    try:
                        self.driver.get(emailVerificationUrl)
                        time.sleep(5)

                        self.printMessage("Please wait while registering account ...")
                        result = Core.register(False, self.info, self.driver)
                        if result == ERROR_RESUME:
                            self.printMessage("Successfully verified, but resume file is not existed")
                            self.writeEmailLog(emailAddress)
                        elif result == ERROR_PHOTO:
                            self.printMessage("Successfully verified, but photo file is not existed")
                            self.writeEmailLog(emailAddress)           
                        elif result == SUCCESS_SIGNUP: 
                            self.printMessage("Successfully signup completed.")
                            self.writeEmailLog(emailAddress)
                        else: 
                            self.printMessage("Successfully verified, but Unexpected Error.")
                    except TimeoutException as e:
                        self.printMessage("Email verification has been failed.")
                        result = ERROR_EMAIL_VERIFY

                    if result == SUCCESS_SIGNUP: return True
                    return False
                else: 
                    self.printMessage("Error occurs while register")
                    return False
            else:
                self.printMessage('Error occurs while singup')
                return False
        except Exception as e: 
            print(e)
            self.printMessage("Something went wrong")
            return False

    def login(self):
        email = self.emailEdit.text()
        if email.strip() == '':
            self.printMessage('Please input email address to log in')
            return
        try:            
            self.printMessage("Please wait while login ... ")
            result = Core.login(email, self.info, self.driver)
            if result: 
                self.printMessage("Successfully Loged in")
            else: 
                self.printMessage("Unexpected Error in login")
            return result
        except: 
            self.printMessage("Something went wrong")
            return False
        
    