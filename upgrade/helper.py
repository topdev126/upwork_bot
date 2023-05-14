import sys, os, getpass, shutil
import time
import imaplib2
import string    
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import ChromeOptions

from constants import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def getChromeDriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('-headless-')
    # dPath = os.path.join(os.path.dirname(__file__), "./chromedriver")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = Chrome(options=chrome_options)
    
    # driver = Chrome(executable_path=dPath, options=chrome_options)

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source":
            "const newProto = navigator.__proto__;"
            "delete newProto.webdriver;"
            "navigator.__proto__ = newProto;"
    })
    return driver

def getUpworkVerifyLink(email, user, password):
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
        con = imaplib2.IMAP4_SSL(IMAP_URL)
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
                        except UnicodeEncodeError as e: 
                            print(e)
                            pass
            if isFound: break
            time.sleep(5)
        return verifyLink
    except: return False 

def generateFakeEmail(email, count):
    splitEmail = email.split('@')
    newEmail = splitEmail[0] + '+' + generateRandomString(count) + '@' + splitEmail[1]
    return newEmail 

def generateRandomString(count):
  return ''.join(random.choices(string.ascii_lowercase + string.digits, k = count)) 

def type_keys(element: WebElement, text: str):
    delay = random.uniform(0.1, 0.5)
    element.send_keys(text)
    time.sleep(delay)  

def getResponseFromGPT(description, apiKey):
    import openai
    openai.api_key = apiKey
    # with open("aiMessages.txt") as f:
    #     ref_text = f.read()
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt='\nQ:'+description+"\nA:",
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
    )

    return response['choices'][0]['text']  