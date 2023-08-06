from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.options import Options

import os
from pathlib import Path

def uploadModel(username='dsw@i-wunder.com', password='dsw', fileModelPath = "saved_models/randomforest_with_advertising.pkl"):
    
    filePath = os.getcwd().replace("\\","/")+"/"+fileModelPath
    p = Path(filePath)
    
    if (p.exists()):

        url = "https://load.staging.apps.i-wunder.com/"   #"https://load.workbench.i-wunder.com/"


        chrome_options = Options()
        chrome_options.add_argument("--headless")

        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)

        delay = 3 # seconds

        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'username')))
                        
            element=browser.find_element(By.ID,"username").send_keys(username)
            element=browser.find_element(By.ID,"password").send_keys(password)

            browser.find_element(By.ID,'kc-login').click()
            

            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'data')))
            button = browser.find_element("xpath","//input[@type='file']")
            browser.execute_script("arguments[0].style.display = 'block';", button)

                        
            button.send_keys(filePath)
            browser.find_element(By.ID,'upload-btn').click()
            print("Uploading...")
            
            notify="uploaded successfully!"
            myElem = WebDriverWait(browser, delay+30).until(EC.text_to_be_present_in_element((By.ID,'info'), notify))
        
            if myElem:
                print("Model uploaded successfully.")
                browser.close()
                return True
            else:
                print("Upload basarisiz!!!!!")
                browser.quit()
                return False
        except TimeoutException:
            print("Loading took too much time!")
            return False

    else:
        print("Modelpath ist nicht korrekt.")



