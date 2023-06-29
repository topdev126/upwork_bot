import sys, os, getpass, shutil
import time
import imaplib2
import string    
import random
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

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

def getGptDriver():
    driver = uc.Chrome(headless=True,use_subprocess=False)
    driver.get("https://chatbot.theb.ai/")
    driver.implicitly_wait(10)

    return driver 

def deletePrivGptChat(driver):
    # delete chat
    W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[@class='p-1']")))
    driver.find_elements(By.XPATH, "//button[@class='p-1']")[-1].click()
    confirmButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='n-button n-button--primary-type n-button--small-type']")))
    confirmButton.click()   
    
    
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
        while(count < 20):
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
                            data = data.replace('=\r\n', '')
                            data = data.replace('=3D', '=')
                            spos = data.find('href="https://www.upwork.com/nx/signup/verify-email/token/')
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
def getRespFromBaiChat(driver, description, props):
    if props != 'ques':
        # delete previous gpt chat 
        deletePrivGptChat(driver)
    queryBar = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@class='n-input__textarea-el']")))
    type_keys(queryBar, description)
    submitButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='n-button n-button--primary-type n-button--medium-type']")))
    submitButton.click()
    time.sleep(6)
    try:
        answer = driver.find_elements(By.XPATH, "//div[@class='flex w-full mb-6 overflow-hidden']")[-1].text
        answer = '\n'.join(answer.split('\n')[1:])
    except: answer = ""

    answer = filterAnswer(answer, props)
    
    return answer

def filterAnswer(answer, props):
    
    answerList = answer.split('\n')
    start_ind_1, start_ind_2, end_ind_1, end_ind_2 = 0, 0, len(answerList)-1, len(answerList)-1
    for i, ans in enumerate(answerList):
        if "[Client]" in ans or "Dear" in ans:
            start_ind_1 = i + 1        
        if "AI language model" in ans:
            start_ind_2 = i + 1
        if "Thank you" in ans:
            end_ind_1 = i
        if "[Your Name]" in ans:
            end_ind_2 = i            
    start_ind = max(start_ind_1, start_ind_2)
    end_ind = min(end_ind_1, end_ind_2)
    if props == 'ques' and end_ind - start_ind > 4: end_ind = start_ind + 4
    if end_ind >= start_ind: 
        result = '\n'.join(answerList[start_ind:end_ind])
    else:
        result = '\n'.join(answerList[start_ind:start_ind+1])
    return result