from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import os
import re

from constants import *
from helper import *

class Core():
    @staticmethod
    def login(email, info, driver):
        if driver is None:
            return ERROR_BROWSER
            
        try:
            driver.get(LOGIN_PATH)
        except TimeoutException as e:
            print("DEBUG: Proxy or Connection Error: " + str(e))

        # cookie acception 
        time.sleep(5)
        try:
            acceptCookiesBtn = W(driver, 220).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            driver.execute_script('arguments[0].click()', acceptCookiesBtn)
        except: pass
        try:
            try:
                userEmail = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_username']")))
                continueToPass = W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[@id='login_password_continue']")))
                type_keys(userEmail, email)
                time.sleep(0.7)
                continueToPass.click()
            except: pass
            time.sleep(1)
            password = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_password']")))
            type_keys(password, info['password'])
            time.sleep(0.5)
            continueToLogin = W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[@id='login_control_continue']")))
            continueToLogin.click()
            time.sleep(3)

            # protect your account
            
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), \"Let's make sure it's you\" ) ]"))):
                    loginAnswer = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@id='login_answer']")))
                    type_keys(loginAnswer, info['secretKey'])
                    next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@id='login_control_continue']")))
                    next.click() 
            except: pass
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Protect your account' ) ]"))):
                    protectNextButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='control_continue']")))
                    protectNextButton.click()
            except: pass
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Scan this QR Code or request a key' ) ]"))):
                    protectSkipButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='control_cancel']")))
                    protectSkipButton.click()
            except: pass
            # Receive a prompt on your Upwork mobile app
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Receive a prompt on your Upwork mobile app' ) ]"))):
                    protectSkipButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='control_cancel']")))
                    protectSkipButton.click()
            except: pass
            # Security preference confirmed
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Security preference confirmed' ) ]"))):
                    protectDoneButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@id='control_continue']")))
                    protectDoneButton.click()
            except: pass
            # check if logining
            try:
                W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")))
                return True
            except: return False
        except: return False
 
    @staticmethod
    def signUp(email, info, driver):
        if driver is None:
            return ERROR_BROWSER

        try:
            driver.get(SIGNUP_PATH)
        except TimeoutException as e:
            print("DEBUG: Proxy or Connection Error: " + str(e))
        # cookie acception 
        time.sleep(5)
        try:
            acceptCookiesBtn = W(driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            acceptCookiesBtn.click()
        except: pass

        # selection of freelancer or client
        selectElement = driver.find_elements(By.XPATH, "//div[@class='up-button-box-label']")[1]
        
        time.sleep(1)
        selectElement.click()
        time.sleep(0.5)
        applyFree = driver.find_elements(By.XPATH, "//button[@class='up-btn up-btn-primary width-md up-btn-block']")[0]
        applyFree.click()
        firstNameInput = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='first-name-input']")))
        lastNameInput = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='last-name-input']")))
        emailInput = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='redesigned-input-email']")))
        passwordInput = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password-input']")))
        checkUpPolicy = driver.find_elements(By.XPATH, "//label[@class='up-checkbox-label']")[1]
        submitButton = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@id='button-submit-form']")))
        firstName, lastName, password, country = info['firstName'], info['lastName'], info['password'], info['country']
        type_keys(firstNameInput, firstName)
        time.sleep(0.5)
        type_keys(lastNameInput, lastName)
        time.sleep(0.5)
        type_keys(emailInput, email)
        time.sleep(0.5)
        type_keys(passwordInput, password)
        time.sleep(0.5)
        # country setting
        W(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='country-dropdown']"))).click()
        countryInput = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))
        countryInput.click()
        type_keys(countryInput, country)
        time.sleep(0.5)
        countryInput.send_keys(Keys.ARROW_DOWN)
        W(driver, 3).until(EC.element_to_be_clickable((By.XPATH,f"//ul[@role='listbox']/li/span/span[contains(text(), '{country}')]"))).click()
        checkUpPolicy.click()
        time.sleep(0.5)
        submitButton.click()
        time.sleep(15)
        try:
            W(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@id='collapseChangeEmailButton']")))
            return True
        except: return False

    @staticmethod
    def register(refresh, info, driver):
        if driver is None:
            return ERROR_BROWSER

        if refresh:
            try:
                driver.get(REGISTER_PATH)
                time.sleep(5)
            except TimeoutException as e:
                print("DEBUG: Proxy or Connection Error: " + str(e))
        try:
            acceptCookiesBtn = W(driver, 4).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            time.sleep(0.5)
            acceptCookiesBtn.click()
        except: pass   

        try:
            # get started 
            getStarted = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn mr-7 air3-btn-primary']")))
            getStarted.click()
            # select level
            W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@data-qa='button-box']")))        
            selectLevel = driver.find_elements(By.XPATH, "//div[@data-qa='button-box']")[2] # expert
            selectLevel.click()
            time.sleep(0.5)
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()
            time.sleep(0.5)
            # select goal
            W(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@class='air3-btn-box-input']")))
            goal =  driver.find_elements(By.XPATH, "//input[@class='air3-btn-box-input']")[2] # fulltime job
            time.sleep(0.5)
            ActionChains(driver).move_to_element(goal).click().perform()
            next = W(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()
            time.sleep(0.5)
            # select method
            W(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@class='air3-btn-box-input']")))
            method =  driver.find_elements(By.XPATH, "//input[@class='air3-btn-box-input']")[1] # clients
            time.sleep(0.5)
            ActionChains(driver).move_to_element(method).click().perform()
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(0.5)

            ### How would you like to tell us about yourself?   
            # resume
            W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='mb-3 air3-btn air3-btn-secondary d-none d-md-block']")))
            resume = driver.find_elements(By.XPATH, "//button[@class='mb-3 air3-btn air3-btn-secondary d-none d-md-block']")[1] # resume
            resume.click()
            resumePath = info['resumePath']
            if not os.path.isfile(resumePath): return ERROR_RESUME # resume file not exist
            resumeUpload = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            resumeUpload.send_keys(resumePath)
            W(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Remove']")))
            resumeContinue = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn air3-btn-primary mb-0']")))
            resumeContinue.click()
            # professional role
            professionalRole = info['professionalRole']
            roleInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='title-label']")))
            ActionChains(driver).move_to_element(roleInput).click().perform()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").perform()
            time.sleep(0.5)
            roleInput.send_keys(Keys.DELETE)
            type_keys(roleInput, professionalRole)
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()     
            time.sleep(1.5)
            # experiences  
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()        
            time.sleep(1.5)
            # education
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()      
            time.sleep(1.5)
            # certification
            try:
                if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Do you have certifications?' ) ]"))):
                    checkbox = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@data-test='checkbox-input']")))
                    checkbox.click()
                    next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
                    next.click() 
            except: pass
            # languages
            langInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[@class='air3-dropdown-toggle-label ellipsis']")))
            langInput.click()
            time.sleep(2)
            languageIndex = info['languageIndex']
            selLang = driver.find_elements(By.XPATH, "//li[@class='air3-menu-item']")[languageIndex] # clients
            selLang.click()
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(2.5)
            # skills
            skills = info['skills']
            skills.insert(0, '')
            for skill in skills:
                try:
                    typeInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='skills-input']")))    
                    type_keys(typeInput, skill)
                    time.sleep(0.5)
                    typeInput = W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='skills-input']")))    
                    typeInput.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.3)
                    selectSkill = W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//li[@class='is-focused is-uncheckable air3-menu-item']")))
                    selectSkill.click()
                except: pass
                
            time.sleep(0.5)
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1.5)  
            # overview
            overview = info['overview']
            overviewInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            overviewInput.clear()
            # ActionChains(driver).move_to_element(overviewInput).click().perform()
            # overviewInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            # ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").perform()
            time.sleep(0.5)
            overviewInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='overview-label']")))
            overviewInput.send_keys(Keys.DELETE)
            type_keys(overviewInput, overview)
            time.sleep(1)
            next = W(driver, 6).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(1.5)
            # categories  
            categories = info['categories']
            # categories.insert(0, 'xxx')
            cateCheck = False
            for category in categories:
                try:
                    cate = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//button[@aria-label='{category}']")))
                    driver.execute_script('arguments[0].click()', cate)
                    cateCheck = True
                except: pass
            if not cateCheck:
                cate = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//button[@class='air3-token mr-2 mb-2 air3-token-multi-select']")))
                driver.execute_script('arguments[0].click()', cate)
            next = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click()   
            time.sleep(1) 
            # rate
            rate = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, f"//input[@aria-label='Hourly rate in $/hr']")))
            rate.clear()
            houlyWage = info['houlyWage']
            type_keys(rate, houlyWage)
            time.sleep(0.5)  
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1)

            # setting photo and location
            street, city, phone, zipcode = info['street'], info['city'], info['phone'], info['zipCode']
            streetInput = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='street-label']")))
            type_keys(streetInput, street)
            time.sleep(0.5)
            for i in range(2):
                try:
                    cityInput = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='city-label']")))
                    type_keys(cityInput, city)
                    time.sleep(1.5)
                    cityInput = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='city-label']")))
                    cityInput.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.3)
                    selCity = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//li[@class='is-focused is-uncheckable air3-menu-item']")))
                    selCity.click()
                    time.sleep(0.3)
                except: pass

            zipInput = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@aria-labelledby='postal-code-label']")))
            type_keys(zipInput, zipcode)
            time.sleep(0.3)

            phoneInput = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter number']")))
            type_keys(phoneInput, phone)
            time.sleep(0.5)

            # photo
            photobutton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@data-cy='open-loader']")))
            photobutton.click()
            time.sleep(0.5)
            photoPath = info['photoPath']
            if not os.path.isfile(photoPath): return ERROR_PHOTO # photo file not exist
            photoUpload = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            photoUpload.send_keys(photoPath)   
            time.sleep(1)  
            okayButton = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn air3-btn-primary']")))   
            okayButton.click()
            # check your profile
            time.sleep(5)
            next = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-test='step-next-button']")))
            next.click() 
            time.sleep(1)      
            # submit
            submitButton = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='air3-btn width-md m-0 air3-btn-primary']")))
            submitButton.click()

            time.sleep(3)
            # get most-recent page
            findWorkUrl = MOST_RECENT_PATH
            driver.get(findWorkUrl)
            time.sleep(3)
            return SUCCESS_SIGNUP
        except Exception as e: 
            print(e)
            return ERROR_SIGNUP

    @staticmethod
    def autoBid(autoBidIntervalTime, info, driver):
        findWorkUrl = info['findWorkUrl']
        driver.get(findWorkUrl)
        time.sleep(4)
        # try:
        #     closeButton = W(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='up-icon']")))
        #     driver.execute_script('arguments[0].click()', closeButton)
        # except: pass
        
        # refresh
        checkedFile = JOB_CHECK_FILE
        try:
            with open(checkedFile) as f:
                checkedJobs = f.readlines()
                checkedJobs = [v.strip() for v in checkedJobs if v.strip() != '']
        except: checkedJobs = []
        while True:
            try:
                # if stopFlag: break
                driver.refresh()
                time.sleep(1)
                try:
                    if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Buy Connects' ) ]"))):
                        return INSUFFICIENT_CONNECTS
                except: pass
                try:
                    if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Submit a Proposal' ) ]"))):
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                except: pass
                try:
                    W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@data-ev-unique_element_id='t-cfeui_qp_Close_8']"))).click()
                except: pass
                # scrol down
                W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")))
                # driver.execute_script("window.scrollTo(0, 1000)")
                
                # get avaiable connect balances
                # connectBalance = W(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[@data-ev-unique_element_id='t-fwh_connects_AvailableConnectsBalance']"))).text
                # connectBalance = int(re.findall(r'\d+', connectBalance)[0])
                # if connectBalance < 8:
                #     return INSUFFICIENT_CONNECTS # insufficient connect.
                
                # get jobs 
                titles, jobTypes, verifiedLists, links, descriptions = [], [], [], [], []
                sections = driver.find_elements(By.XPATH, "//section[@class='up-card-section up-card-list-section up-card-hover']")
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
                    driver.execute_script(f"window.open('{link}')")            
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(0.5)
                    # get connect count
                    
                    try:
                        connectBalance = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Available Connects' ) ]"))).text
                        connectBalance = int(re.findall(r'\d+', connectBalance)[0])
                        if connectBalance < 8:
                            return INSUFFICIENT_CONNECTS # insufficient connect. 
                    except: pass                   
                    
                    errorCheck = False
                    try:
                        applyButton = W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Apply Now']")))
                        if applyButton.is_enabled():
                            applyButton.click()
                        else: errorCheck = True
                    except: errorCheck = True
                    if errorCheck:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])  
                        continue                      
                    
                    try:
                        # some info dialog
                        closeButton = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn mt-0 mb-0 up-btn-primary']")))
                        closeButton.click()
                    except: pass
                    time.sleep(1.5)
                    try:
                        if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Buy Connects' ) ]"))):
                            return INSUFFICIENT_CONNECTS
                    except: pass
                    if jobTypes[i] == "Fixed-price":
                        try:
                            # by project
                            W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//label[@class='up-checkbox-label']")))
                            radioButton = driver.find_elements(By.XPATH, "//label[@class='up-checkbox-label']")[1]
                            radioButton.click()
                        except: pass
                        # duration
                        time.sleep(0.5)
                        budgetEditbox = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@id='charged-amount-id']")))
                        budget = budgetEditbox.get_attribute('value')
                        budget = float(budget)
                        durationIndex = 0
                        if budget < FIXED_BUDGET_DURATION_LESS_1: 
                            durationIndex = -1
                            budget *= FIXED_BUDGET_PERCENTAGE_LESS_1
                        elif budget < FIXED_BUDGET_DURATION_1_3: 
                            budget *= FIXED_BUDGET_PERCENTAGE_1_3
                            durationIndex = -2
                        elif budget < FIXED_BUDGET_DURATION_3_6: 
                            budget *= FIXED_BUDGET_PERCENTAGE_3_6
                            durationIndex = -3
                        else: 
                            durationIndex = -4
                            budget *= FIXED_BUDGET_PERCENTAGE_MORE_6
                        budgetEditbox.clear()
                        type_keys(budgetEditbox, budget)
                        duration = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@class='up-dropdown-toggle-title']"))) # duration dropdown click
                        duration.click()
                        time.sleep(2)
                        durationOptions = driver.find_elements(By.XPATH, "//li[@role='option']")
                        
                        if len(durationOptions) == 0:
                            duration.click()
                            time.sleep(2)
                            durationOptions = driver.find_elements(By.XPATH, "//li[@role='option']")
                        time.sleep(1)
                        durationOptions[durationIndex].click() #driver.execute_script('arguments[0].click()', acceptCookiesBtn)
                        time.sleep(0.5)
                    else:
                        try:
                            clientRate = float(jobTypes[i].split('$')[-1])
                            if clientRate > float(info['houlyWage']):
                                rate = str(int(float(info['houlyWage']) * 0.5 + float(jobTypes[i].split('$')[-1]) * 0.5)) # 0.5 and 0.5 means weights to calculate final rate
                            else: rate = str(int(clientRate))
                        except: rate = info['houlyWage']
                        if int(rate) < 25: 
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])  
                            continue                          
                        rateInput = driver.find_element(By.XPATH, "//input[@id='step-rate']")
                        rateInput.clear()
                        type_keys(rateInput, rate)
                        time.sleep(0.5)

                    # cover letter
                    coverLetter = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-labelledby='cover_letter_label']")))
                    if "bubble" in descriptions[i].lower():
                        bidContent = info['customBID']['bubble']
                        type_keys(coverLetter, bidContent)
                    else:
                        description = descriptions[i] + "\nGive me Sample my bid content to get this job."
                        bidContent = getResponseFromGPT(description, info['GPTAPIKey'])            
                        time.sleep(5)
                        if len(bidContent) < 50:
                            bidContent = info['initBID']
                        else:
                            bidContent = info['CVHeader'] + "\n\n" + bidContent + "\n\n" + info['CVFooter']
                        type_keys(coverLetter, bidContent)
                    time.sleep(0.5)
                    # some questions:
                    try:
                        questions = driver.find_elements(By.XPATH, "//div[@class='form-group up-form-group']")
                        if len(questions) > 1:
                            for k in range(1, len(questions)):
                                question = questions[k]
                                questionLabel = question.find_element(By.XPATH, ".//label[@class='up-label']").text
                                questionInput = question.find_element(By.XPATH, ".//textarea[@class='up-textarea']")
                                ques = questionLabel + "\nGive me clear answer for this question."
                                if "github" in questionLabel.lower():
                                    type_keys(questionInput, "https://github.com/" + info['githubUsername'])
                                else:
                                    answer = getResponseFromGPT(ques, info['GPTAPIKey'])  
                                    if len(answer) < 5: answer = "    "
                                    time.sleep(1)
                                    type_keys(questionInput, answer)
                    except: pass      
                    time.sleep(0.5)     
                    # boost
                    try:
                        W(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-default m-0']"))).click()
                        time.sleep(0.5)
                        W(driver, 0.5).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-default up-btn-sm m-0']"))).click()
                    except: pass
                    # send
                    bidSend = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-primary m-0']")))
                    bidSend.click()
                    # stay safe & build my reputation
                    try:
                        checkSending = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//input[@name='checkbox']")))
                        checkSending.click()
                        submit = W(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[@class='up-btn up-btn-primary m-0 btn-primary']")))
                        submit.click()  
                        time.sleep(3)
                        try:
                            if W(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[ contains (text(), 'Buy Connects' ) ]"))):
                                return INSUFFICIENT_CONNECTS
                        except: pass                  
                    except: pass

                    checkedJobs.append(titles[i].strip())
                    
                    time.sleep(1.5)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(5)
                # write checkedjobs
                with open(checkedFile, 'w') as f:
                    for line in checkedJobs[-20:]:
                        if line.strip() != '':
                            f.write(f"{line}\n")   

                time.sleep(autoBidIntervalTime * 60)
            except Exception as e: 
                print(e)
                pass
