from PyQt5 import QtWidgets, uic,QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QDialog, QLineEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import sys, os, getpass, shutil
from threading import *
import json
import requests
from upwork import UpworkBot
import time
import imaplib2
import string    
import random # define the random module  

user = 'josecrbtr@gmail.com'
password = 'hryjujwxsoecfwvr'
imap_url = 'imap.gmail.com'

checkEmailFile = 'emails.txt'
suffixCount = 10  # number of characters in the string. 
class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage,self).__init__()
        uic.loadUi(resource_path("include_auto.ui"),self)
        self.setFixedSize(907, 487)

        self.signFlag = False
        self.verfiFlag = False
        self.mainFlag = False
        self.jsonInfos = None
        
        self.initUI() 
    
    def initUI(self):
        self.btn_2.clicked.connect(self.START_1)
        self.btn_4.clicked.connect(self.START_2)
        self.btn_6.clicked.connect(self.START_3)


        self.btn_1.clicked.connect(lambda: self.getConfig(self.label, self.lineEdit_3, self.lineEdit_4, self.lineEdit_13))
        self.btn_3.clicked.connect(lambda: self.getConfig(self.label_2, self.lineEdit_7, self.lineEdit_8, self.lineEdit_14))
        self.btn_5.clicked.connect(lambda: self.getConfig(self.label_3, self.lineEdit_11, self.lineEdit_12, self.lineEdit_15))

        # login

        self.btn_10.clicked.connect(self.login_Start_1)
        self.btn_11.clicked.connect(self.login_Start_2)
        self.btn_12.clicked.connect(self.login_Start_3)

        # auto bid
        self.btn_7.clicked.connect(self.autoBID_1)
        # self.btn_8.clicked.connect(self.autoBID_2)
        # self.btn_9.clicked.connect(self.autoBID_3) 

        # initial disable
        self.btn_7.setEnabled(False) # non active of auto-bid button
        self.btn_8.setEnabled(False) # non active of auto-bid button
        self.btn_9.setEnabled(False) # non active of auto-bid button

        # stop button
        self.btn_13.clicked.connect(lambda : self.OnStop(1))
        self.btn_14.clicked.connect(self.xxxx)
        self.btn_15.clicked.connect(lambda : self.OnStop(3))
        
        self.stop = [False, False, False]

        self.upworkBot = None  
    def Onstop(self, ind):
        self.stop[ind] = True
    def autoBID_1(self) :
        t7=Thread(target=self.autoBID_process, args=(self.label, self.lineEdit_13))
        t7.start()
        # t7.join()
    def xxxx(self):
        checkedFile = '_mail.txt'
        with open(checkedFile) as f:
            emails = f.readlines()
            emails = [v.strip() for v in emails if v.strip() != '']
        for email in emails:
            self.lineEdit.setText(email)
            try:
                self.login_Start_1()
                time.sleep(5)
                self.autoBID_1()
            except:
                print(f"================={email}=================")
    def login_Start_1(self):
        t4=Thread(target=self.PROCESS, args=(self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.label, self.btn_7, 'login', self.lineEdit_13))
        t4.start()
        t4.join
    def login_Start_2(self):
        t5=Thread(target=self.PROCESS, args=(self.lineEdit_5, self.lineEdit_6, self.lineEdit_7, self.lineEdit_8, self.label_2, self.btn_8, 'login', self.lineEdit_13))
        t5.start()
        t5.join
    def login_Start_3(self):
        t6=Thread(target=self.PROCESS, args=(self.lineEdit_9, self.lineEdit_10, self.lineEdit_11, self.lineEdit_12, self.label_3, self.btn_9, 'login', self.lineEdit_13))
        t6.start()
        t6.join                
    def getConfig(self, label, nameIn, countryIn, timeIn):
        configPath, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self, "Open File", "", "CSV Files(*.json);;All Files (*)",
            options=QtWidgets.QFileDialog.DontUseNativeDialog)    
        if configPath is not None: 
            label.setText(f"Config Path: {configPath[0]} ")
            try:
                with open(configPath[0], "r") as f:
                    self.jsonInfos = json.load(f) 
                name = self.jsonInfos['firstName'] + ' ' + self.jsonInfos['lastName']
                country = self.jsonInfos['country']
                autoBIDtime = self.jsonInfos['bidTime']
                nameIn.setText(name)
                countryIn.setText(country)   
                timeIn.setText(autoBIDtime)                          
            except: label.setText(f"Check config file ...")
    def activeBrowser(self,):
        if self.le_tab2_2.text() == '':
            self.btn_browse2.setEnabled(False)
            self.le_tab2.setEnabled(False)
        else: 
            self.btn_browse2.setEnabled(True)
            # self.le_tab2.setEnabled(True)
    def openOutput(self,path): 
        if path:  
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(path)))
    def START_1(self):
        t1=Thread(target=self.PROCESS, args=(self.lineEdit, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.label, self.btn_2, 'signUp', self.lineEdit_13))
        t1.start()
        t1.join
    def START_2(self):
        t2=Thread(target=self.PROCESS, args=(self.lineEdit_5, self.lineEdit_6, self.lineEdit_7, self.lineEdit_8, self.label_2, self.btn_4, 'signUp', self.lineEdit_13))
        t2.start()
        t2.join
    def START_3(self):
        t3=Thread(target=self.PROCESS, args=(self.lineEdit_9, self.lineEdit_10, self.lineEdit_11, self.lineEdit_12, self.label_3, self.btn_6, 'signUp', self.lineEdit_13))
        t3.start()
        t3.join    
    def getVerifyLink(self, email):
        try:
            # Function to get email content part i.e its body part
            def get_body(msg):
                if msg.is_multipart():
                    return get_body(msg.get_payload(0))
                else:
                    return msg.get_payload(None, True)
            # Function to search for a key value pair
            def search(key, value, con):
                result, data = con.search(None, key, '"{}"'.format(value))
                return data
            # Function to get the list of emails under this label
            def get_emails(result_bytes):
                msgs = [] # all the email data are pushed inside an array
                for num in result_bytes[0].split():
                    typ, data = con.fetch(num, '(RFC822)')
                    msgs.append(data)

                return msgs

            # this is done to make SSL connection with GMAIL
            con = imaplib2.IMAP4_SSL(imap_url)
            # logging the user in
            con.login(user, password)
            # calling function to check for email under this label
            con.select('Inbox')

            time.sleep(2)
            count = 0
            verifyLink = False
            while(count < 10):
                count += 1
                msgs = get_emails(search('TO', email, con))

                isFound = False
                # printing them by the order they are displayed in your gmail
                for msg in msgs[::-1]:
                    for sent in msg:
                        if type(sent) is tuple:

                            # encoding set as utf-8
                            content = str(sent[1], 'utf-8')
                            data = str(content)

                            # Handling errors related to unicodenecode
                            try:
                                spos = data.find('href=3D"https://www.upwork.com/nx/signup/verify-emai=\r\nl/token/')
                                spos += 50
                                data2 = data[spos : spos + 60]
                                token = data2.split('">')[0]
                                token = token.split('token/')[1]
                                verifyLink = 'https://www.upwork.com/nx/signup/verify-email/token/' + token
                                isFound = True
                                break
                            except UnicodeEncodeError as e: pass
                if isFound: break
                time.sleep(5)
            return verifyLink
        except: return False    
    def generateEmail(self, email):
        def generateRandom():
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k = suffixCount))   
        checkEmails = []
        try:
            with open(checkEmailFile) as f:
                checkEmails = f.readlines()
                checkEmails = [v.strip() for v in checkEmails if v.strip() != '']
        except: checkEmails = []
        splitEmail = email.split('@')
        newEmail = splitEmail[0] + '+' + generateRandom() + '@' + splitEmail[1]
        while(newEmail in checkEmails):
            newEmail = email + '+' + generateRandom()
        return newEmail
    def writeEmailLog(self, email):
        with open(checkEmailFile, 'a') as f:
            f.write(f"{email}\n")  
    def autoBID_process(self, label, timeIn):
        label.setText("Starting auto bid ... ")
        try:
            self.jsonInfos['bidTime'] = timeIn.text()
            result = self.upworkBot.autoBID()
            if result == 131:
                label.setText("Insufficient connect balances.")
            elif result == 130:
                label.setText("Unexpected Error in auto bid ... ")
            else: label.setText("Something went wrong")
        except: 
            label.setText("Unexpected Error in auto bid ... ")
    def PROCESS(self, emailIn, emailIn2, nameIn, countryIn, label, processbtn, props, autoTimeIn):
        label.setText("")
        if props == 'signUp':
            if not self.signFlag:
                try:
                    email = emailIn.text()
                    emailAddress = self.generateEmail(user)
                    #emailAddress = email
                    emailIn2.setText(emailAddress)
                    self.jsonInfos['firstName'], self.jsonInfos['lastName'] = nameIn.text().split(' ')
                    self.jsonInfos['country'] = countryIn.text()
                    label.setText("Please wait while signing up ... ")
                    self.upworkBot = UpworkBot(self.jsonInfos)
                    su = self.upworkBot.signUp(emailAddress)
                    if su:
                        label.setText("Verify your email address")
                        emailIn.setPlaceholderText("Email Verification Code")
                        emailIn.setText("")
                        processbtn.setText("Next")
                        self.signFlag = True
                        self.btn_7.setEnabled(True) # active of auto-bid button
                        label.setText("Verifying email...")

                        emailVerificationCode = self.getVerifyLink(emailAddress)
                        if emailVerificationCode != False:
                            result = self.upworkBot.emailVerifyAndMain(emailVerificationCode)
                            if result == 101:
                                label.setText("Verification has been failed.")
                            elif result == 102:
                                label.setText("Successfully verified, but resume file is not existed")
                                self.writeEmailLog(emailAddress)
                                emailIn.setText("")
                                # self.verfiFlag = True
                            elif result == 103:
                                label.setText("Successfully verified, but photo file is not existed")
                                self.writeEmailLog(emailAddress)
                                emailIn.setText("")                
                            elif result == 200: 
                                label.setText("Successfully completed.")
                                self.writeEmailLog(emailAddress)
                                self.autoBID_process(label, autoTimeIn)
                                emailIn.setText("")
                            else: 
                                label.setText("Successfully verified, but Unexpected Error.")
                                emailIn.setText("")

                            self.signFlag, self.verfiFlag = False, False
                        else: label.setText("Error !!!")
                except Exception as e: 
                    print(e)
                    label.setText("Select exact config file ...")
            elif not self.verfiFlag:
                emailVerificationCode = emailIn.text() 
                label.setText("Please wait while ...")
                result = self.upworkBot.emailVerifyAndMain(emailVerificationCode)
                if result == 101:
                    label.setText("Verification has been failed.")
                elif result == 102:
                    label.setText("Successfully verified, but resume file is not existed")
                    emailIn.setText("")
                    # self.verfiFlag = True
                elif result == 103:
                    label.setText("Successfully verified, but photo file is not existed")
                    emailIn.setText("")                
                elif result == 200: 
                    label.setText("Successfully completed.")
                    emailIn.setText("")
                else: 
                    label.setText("Successfully verified, but Unexpected Error.")
                    emailIn.setText("")

                self.signFlag, self.verfiFlag = False, False
        else:
            try:
                email = emailIn.text()
                emailIn2.setText(email)
                self.jsonInfos['firstName'], self.jsonInfos['lastName'] = nameIn.text().split(' ')
                self.jsonInfos['country'] = countryIn.text()
                label.setText("Please wait while login ... ")
                self.upworkBot = UpworkBot(self.jsonInfos)
                su = self.upworkBot.login(email)
                if su: 
                    label.setText("Successfully Logined")
                    emailIn.setText("")
                    processbtn.setEnabled(True) # active of auto-bid button
                else: 
                    label.setText("Unexpected Error in login")
                    emailIn.setText("")
            except: 
                label.setText("Select exact config file ...")
    
    def onChangeValue2(self,val):
        self.pbar_tab2.setFormat(str(self.cnt2) + '/' + str(self.total2))

    single_done2 = pyqtSignal()
    @pyqtSlot()    
    def progress2(self):
        self.pbar_tab2.setValue(int((self.cnt2/self.total2)*100))

    def openFolder2(self, path):
        self.label.setText("Result : Successfully processed "+ str(self.totol2) +" files")
        self.path2=path
        self.lnk_tab2.setText(str(path))
        self.openOutput(path)
    
    def onClickLblTab2(self):
        self.openOutput(self.path2)
        #QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(path)))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def makedir(dir):
    try:
        os.mkdir(dir)
    except:
        pass
def window():
    app = QApplication(sys.argv)
    win = MainPage()
    win.show()
    sys.exit(app.exec_())
    
window()    