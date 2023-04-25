from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import time
import random
import os, json
import re
# from pynput.keyboard import Key, Controller as KeyboardController
# keyboard = KeyboardController()
class UpworkBot():
    def __init__(self, jsonInfos):
        self.driver = None
        self.driverFun()
        self.Infos = jsonInfos

    def type_keys(self, element: WebElement, text: str):
        delay = random.uniform(0.1, 0.5)
        element.send_keys(text)
        time.sleep(delay)

    def driverFun(self,):
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('-headless-')
        # dPath = os.path.join(os.path.dirname(__file__), "./chromedriver")
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = Chrome(options=chrome_options)
        
        # driver = Chrome(executable_path=dPath, options=chrome_options)

        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })
    def login(self, email):
        try:
            self.driver.get("https://www.upwork.com/ab/account-security/login")
        except TimeoutException as e:
            print("DEBUG: Proxy or Connection Error: " + str(e))
        # human verify
        # ActionChains(driver).move_by_offset(X,Y).click().perform()
        
        # humanCheck = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']")))
        # humanCheck.click()

        # cookie acception 
        time.sleep(5)
        try:
            acceptCookiesBtn = W(self.driver, 220).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            self.driver.execute_script('arguments[0].click()', acceptCookiesBtn)
        except: pass
        try:
            try:
                userEmail = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_username']")))
                continueToPass = W(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[@id='login_password_continue']")))
                self.type_keys(userEmail, email)
                time.sleep(0.7)
                continueToPass.click()
            except: pass
            time.sleep(1)
            password = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_password']")))
            self.type_keys(password, self.Infos['password'])
            time.sleep(0.5)
            continueToLogin = W(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[@id='login_control_continue']")))
            continueToLogin.click()
            time.sleep(3)
            # check if logining
            try:
                W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")))
                return True
            except: return False
        except: return False
        
    def signUp(self, email):
        try:
            self.driver.get("https://www.upwork.com/nx/signup/?dest=home")
        except TimeoutException as e:
            print("DEBUG: Proxy or Connection Error: " + str(e))
        # cookie acception 
        time.sleep(5)
        try:
            acceptCookiesBtn = W(self.driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            acceptCookiesBtn.click()
        except: pass

        # selection of freelancer or client
        selectElement = self.driver.find_elements(By.XPATH, "//div[@class='up-button-box-label']")[1]
        
        time.sleep(1)
        selectElement.click()
        time.sleep(0.5)
        applyFree = self.driver.find_elements(By.XPATH, "//button[@class='up-btn up-btn-primary width-md up-btn-block']")[0]
        applyFree.click()
        firstNameInput = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='first-name-input']")))
        lastNameInput = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='last-name-input']")))
        emailInput = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='redesigned-input-email']")))
        passwordInput = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password-input']")))
        checkUpPolicy = self.driver.find_elements(By.XPATH, "//label[@class='up-checkbox-label']")[1]
        submitButton = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='button-submit-form']")))
        firstName, lastName, password, country = self.Infos['firstName'], self.Infos['lastName'], self.Infos['password'], self.Infos['country']
        self.type_keys(firstNameInput, firstName)
        time.sleep(0.5)
        self.type_keys(lastNameInput, lastName)
        time.sleep(0.5)
        self.type_keys(emailInput, email)
        time.sleep(0.5)
        self.type_keys(passwordInput, password)
        time.sleep(0.5)
        # country setting
        W(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='country-dropdown']"))).click()
        countryInput = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        countryInput.click()
        self.type_keys(countryInput, country)
        time.sleep(0.5)
        countryInput.send_keys(Keys.ARROW_DOWN)
        W(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,f"//ul[@role='listbox']/li/span/span[contains(text(), '{country}')]"))).click()
        checkUpPolicy.click()
        time.sleep(0.5)
        submitButton.click()
        time.sleep(15)
        try:
            W(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@id='collapseChangeEmailButton']")))
            return True
        except: return False
                
    def emailVerifyAndMain(self, url):
        try:
            self.driver.get(url)
            time.sleep(5)
        except TimeoutException as e:
            print("DEBUG: Proxy or Connection Error: " + str(e)) 
            return 101
    # def mainBot(self):
        # cookies accept
        time.sleep(3)
        try:
            acceptCookiesBtn = W(self.driver, 4).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            acceptCookiesBtn.click()
        except: pass   

        try:
            # get started 
            getStarted = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn mr-7 air3-btn-primary']")))
            getStarted.click()
            # select level
            W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-qa='button-box']")))        
            selectLevel = self.driver.find_elements(By.XPATH, "//div[@data-qa='button-box']")[2] # expert
            selectLevel.click()
            time.sleep(0.5)
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()
            time.sleep(0.5)
            # select goal
            W(self.driver, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@class='air3-btn-box-input']")))
            goal =  self.driver.find_elements(By.XPATH, "//input[@class='air3-btn-box-input']")[2] # fulltime job
            time.sleep(0.5)
            ActionChains(self.driver).move_to_element(goal).click().perform()
            next = W(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()
            time.sleep(0.5)
            # select method
            W(self.driver, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@class='air3-btn-box-input']")))
            method =  self.driver.find_elements(By.XPATH, "//input[@class='air3-btn-box-input']")[1] # clients
            time.sleep(0.5)
            ActionChains(self.driver).move_to_element(method).click().perform()
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(0.5)

            ### How would you like to tell us about yourself?   
            # resume
            W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='mb-3 air3-btn air3-btn-secondary d-none d-md-block']")))
            resume = self.driver.find_elements(By.XPATH, "//button[@class='mb-3 air3-btn air3-btn-secondary d-none d-md-block']")[1] # resume
            resume.click()
            resumePath = self.Infos['resumePath']
            if not os.path.isfile(resumePath): return 102 # resume file not exist
            resumeUpload = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            resumeUpload.send_keys(resumePath)
            W(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Remove']")))
            resumeContinue = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn air3-btn-primary mb-0']")))
            resumeContinue.click()
            # professional role
            professionalRole = self.Infos['professionalRole']
            roleInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='title-label']")))
            ActionChains(self.driver).move_to_element(roleInput).click().perform()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").perform()
            time.sleep(0.5)
            roleInput.send_keys(Keys.DELETE)
            self.type_keys(roleInput, professionalRole)
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()     
            time.sleep(1.5)
            # experiences  
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()        
            time.sleep(1.5)
            # education
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()      
            time.sleep(1.5)
            # languages
            langInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='air3-dropdown-toggle-label ellipsis']")))
            langInput.click()
            time.sleep(0.3)
            languageIndex = self.Infos['languageIndex']
            selLang = self.driver.find_elements(By.XPATH, "//li[@class='air3-menu-item']")[languageIndex] # clients
            selLang.click()
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(2.5)
            # skills
            skills = self.Infos['skills']
            skills.insert(0, 'xxx')
            for skill in skills:
                try:
                    typeInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='skills-input']")))    
                    self.type_keys(typeInput, skill)
                    time.sleep(0.5)
                    typeInput = W(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='skills-input']")))    
                    typeInput.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.3)
                    selectSkill = W(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//li[@class='is-focused is-uncheckable air3-menu-item']")))
                    selectSkill.click()
                except: pass
                
            time.sleep(0.5)
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1.5)  
            # overview
            overview = self.Infos['overview']
            overviewInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            overviewInput.clear()
            # ActionChains(self.driver).move_to_element(overviewInput).click().perform()
            # overviewInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            # ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").perform()
            time.sleep(0.5)
            overviewInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            overviewInput.send_keys(Keys.DELETE)
            self.type_keys(overviewInput, overview)
            time.sleep(0.3)
            next = W(self.driver, 6).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(1.5)
            # categories  
            categories = self.Infos['categories']
            # categories.insert(0, 'xxx')
            cateCheck = False
            for category in categories:
                try:
                    cate = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{category}']")))
                    self.driver.execute_script('arguments[0].click()', cate)
                    cateCheck = True
                except: pass
            if not cateCheck:
                cate = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//button[@class='air3-token mr-2 mb-2 air3-token-multi-select']")))
                self.driver.execute_script('arguments[0].click()', cate)
            next = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(1) 
            # rate
            rate = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//input[@aria-label='Hourly rate in $/hr']")))
            rate.clear()
            houlyWage = self.Infos['houlyWage']
            self.type_keys(rate, houlyWage)
            time.sleep(0.5)  
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1)

            # setting photo and location
            street, city, phone, zipcode = self.Infos['street'], self.Infos['city'], self.Infos['phone'], self.Infos['zipCode']
            streetInput = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='street-label']")))
            self.type_keys(streetInput, street)
            time.sleep(0.5)
            for i in range(2):
                try:
                    cityInput = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='city-label']")))
                    self.type_keys(cityInput, city)
                    time.sleep(1.5)
                    cityInput = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='city-label']")))
                    cityInput.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.3)
                    selCity = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//li[@class='is-focused is-uncheckable air3-menu-item']")))
                    selCity.click()
                    time.sleep(0.3)
                except: pass

            zipInput = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='postal-code-label']")))
            self.type_keys(zipInput, zipcode)
            time.sleep(0.3)

            phoneInput = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter number']")))
            self.type_keys(phoneInput, phone)
            time.sleep(0.5)

            # photo
            photobutton = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@data-cy='open-loader']")))
            photobutton.click()
            time.sleep(0.5)
            photoPath = self.Infos['photoPath']
            if not os.path.isfile(photoPath): return 103 # photo file not exist
            photoUpload = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            photoUpload.send_keys(photoPath)   
            time.sleep(1)  
            okayButton = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn air3-btn-primary']")))   
            okayButton.click()
            # check your profile
            time.sleep(5)
            next = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1)      
            # submit
            submitButton = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn width-md m-0 air3-btn-primary']")))
            submitButton.click()

            time.sleep(3)
            # get most-recent page
            findWorkUrl = "https://www.upwork.com/nx/find-work/most-recent"
            self.driver.get(findWorkUrl)
            time.sleep(3)
            return 200
        except: return 199
    def autoBID(self):
        findWorkUrl = "https://www.upwork.com/nx/find-work/most-recent"
        self.driver.get(findWorkUrl)
        time.sleep(4)
        # try:
        #     closeButton = W(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='up-icon']")))
        #     self.driver.execute_script('arguments[0].click()', closeButton)
        # except: pass
        
        # refresh
        checkedFile = 'checked.txt'
        try:
            with open(checkedFile) as f:
                checkedJobs = f.readlines()
                checkedJobs = [v.strip() for v in checkedJobs if v.strip() != '']
        except: checkedJobs = ['xxxx']
        while True:
            try:
                # if stopFlag: break
                self.driver.refresh()
                try:
                    W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ev-unique_element_id='t-cfeui_qp_Close_8']"))).click()
                except: pass
                # scrol down
                W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")))
                self.driver.execute_script("window.scrollTo(0, 1000)")
                # get avaiable connect balances
                connectBalance = W(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[@data-ev-unique_element_id='t-fwh_connects_AvailableConnectsBalance']"))).text
                connectBalance = int(re.findall(r'\d+', connectBalance)[0])
                if connectBalance < 6:
                    return 131 # insufficient connect.
                
                # get jobs 
                titles, jobTypes, verifiedLists, links, descriptions = [], [], [], [], []
                sections = self.driver.find_elements(By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")
                for i in range(len(sections)):
                    if i > 9: break
                    section = sections[i]
                    title = section.find_element(By.XPATH, ".//h3[@class='my-0 p-sm-right job-tile-title']").text
                    if title.strip() in  checkedJobs: break
                    veri = section.find_element(By.XPATH, ".//strong[@class='text-muted']").text
                    if veri == 'Payment unverified': continue
                    jobType = section.find_element(By.XPATH, ".//strong[@data-test='job-type']").text
                    if jobType == "Fixed-price":
                        try:
                            budget = section.find_element(By.XPATH, ".//span[@data-test='budget']").text
                            budget = budget[1:].replace(',', '')
                            budget = float(budget)
                        except: budget = 200.0
                        if budget < 400: continue
                    
                    titles.append(title)
                    jobTypes.append(jobType)
                    descriptions.append(section.find_element(By.XPATH, ".//div[@data-test='job-description-line-clamp']").text)
                    # verifiedLists.append(veri)
                    links.append(section.find_element(By.XPATH, ".//a").get_attribute('href'))
                 
                # check every link
                for i, link in enumerate(links):
                    self.driver.execute_script(f"window.open('{link}')")            
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(0.5)
                    # get connect count
                    
                    connectBalance = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='up-card-section actions-section']/div[2]/div[2]"))).text
                    connectBalance = int(re.findall(r'\d+', connectBalance)[0])
                    if connectBalance < 6:
                        return 131 # insufficient connect.                    
                    
                    errorCheck = False
                    try:
                        applyButton = W(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Apply Now']")))
                        if applyButton.is_enabled():
                            applyButton.click()
                        else: errorCheck = True
                    except: errorCheck = True
                    if errorCheck:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])  
                        continue                      
                    
                    try:
                        # some info dialog
                        closeButton = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn mt-0 mb-0 up-btn-primary']")))
                        closeButton.click()
                    except: pass
                    time.sleep(1.5)
                    if jobTypes[i] == "Fixed-price":
                        # by project
                        W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//label[@class='up-checkbox-label']")))
                        radioButton = self.driver.find_elements(By.XPATH, "//label[@class='up-checkbox-label']")[1]
                        radioButton.click()
                        # duration
                        time.sleep(0.5)
                        duration = self.driver.find_elements(By.XPATH, "//span[@class='flex-1 ellipsis']")[0] # duration dropdown click
                        duration.click()
                        time.sleep(0.5)
                        durationOptions = self.driver.find_elements(By.XPATH, "//li[@role='option']")
                        durationOptions[-1].click() #self.driver.execute_script('arguments[0].click()', acceptCookiesBtn)
                        time.sleep(0.5)
                    else:
                        try:
                            clientRate = float(jobTypes[i].split('$')[-1])
                            if clientRate > float(self.Infos['houlyWage']):
                                rate = str(int(float(self.Infos['houlyWage']) * 0.5 + float(jobTypes[i].split('$')[-1]) * 0.5)) # 0.5 and 0.5 means weights to calculate final rate
                            else: rate = str(int(clientRate))
                        except: rate = self.Infos['houlyWage']
                        if int(rate) < 25: 
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])  
                            continue                          
                        rateInput = self.driver.find_element(By.XPATH, "//input[@id='step-rate']")
                        rateInput.clear()
                        self.type_keys(rateInput, rate)
                        time.sleep(0.5)

                    # cover letter
                    coverLetter = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='cover_letter_label']")))
                    if "bubble" in descriptions[i].lower():
                        bidContent = self.Infos['customBID']['bubble']
                        self.type_keys(coverLetter, bidContent)
                    else:
                        description = descriptions[i] + "\nGive me Sample my bid content to get this job."
                        bidContent = self.getBID(description)            
                        time.sleep(5)
                        if len(bidContent) < 50:
                            bidContent = self.Infos['initBID']
                        else:
                            bidContent = self.Infos['CVHeader'] + "\n\n" + bidContent + "\n\n" + self.Infos['CVFooter']
                        self.type_keys(coverLetter, bidContent)
                    time.sleep(0.5)
                    # some questions:
                    try:
                        questions = self.driver.find_elements(By.XPATH, "//div[@class='form-group up-form-group']")
                        if len(questions) > 1:
                            for k in range(1, len(questions)):
                                question = questions[k]
                                questionLabel = question.find_element(By.XPATH, ".//label[@class='up-label']").text
                                questionInput = question.find_element(By.XPATH, ".//textarea[@class='up-textarea']")
                                ques = questionLabel + "\nGive me clear answer for this question."
                                if "github" in questionLabel.lower():
                                    self.type_keys(questionInput, "https://github.com/" + self.Infos['githubUsername'])
                                else:
                                    answer = self.getBID(ques)  
                                    if len(answer) < 5: answer = "    "
                                    time.sleep(1)
                                    self.type_keys(questionInput, answer)
                    except: pass      
                    time.sleep(0.5)     
                    # boost
                    try:
                        W(self.driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-default m-0']"))).click()
                        time.sleep(0.5)
                        W(self.driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-default up-btn-sm m-0']"))).click()
                    except: pass
                    # send
                    bidSend = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-primary m-0']")))
                    bidSend.click()
                    # stay safe & build my reputation
                    try:
                        checkSending = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@name='checkbox']")))
                        checkSending.click()
                        submit = W(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-primary m-0 btn-primary']")))
                        submit.click()                    
                    except: pass

                    checkedJobs.append(titles[i].strip())
                    
                    time.sleep(1.5)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(5)
                # write checkedjobs
                with open(checkedFile, 'w') as f:
                    for line in checkedJobs[-20:]:
                        if line.strip() != '':
                            f.write(f"{line}\n")   

                time.sleep(int(self.Infos['bidTime'])*60)
            except: return 130

    def getBID(self, description):
        import openai
        openai.api_key = "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"
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
def main():
    upworkBot = UpworkBot()
    su = upworkBot.signUp()
    upworkBot.emailVerify(url)
    upworkBot.mainBot()

    # https://www.upwork.com/signup/verify-email/token/VuDR9cejmf?frkscc=w5mah3jPMGGl

#  x = self.driver.switch_to.active_element()
# main()