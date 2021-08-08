from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from variables import *
import pandas as pd

def removeSiteObstructions(driver):
    driver.execute_script("""
                var l = document.getElementById("chat-icon-img");
                    l.remove();
                    """)

def findNoOfResultsInPage(driver):
    containers = driver.find_elements_by_xpath('//div[@class="col-md-6"]')
    resultsInPageCount = len(containers)
    return resultsInPageCount

def waitForChildContainerLoad(driver,elementNo):
    try:

        wait = WebDriverWait(driver, 15, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        elem = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="col-md-6"][' + str(elementNo) + ']/a')))

        # elem = WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="col-md-6"][' + str(elementNo) + ']/a'))
    except:
        print("Timeout while waiting for child container to load")

def waitForParentContainerLoad(driver):
    try:
        wait = WebDriverWait(driver, 15, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        elem = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="col-md-6"]')))
        
        # elem = WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@class="col-md-9"]'))

    except:
        print("Timeout while waiting for parent container to load")

def waitForProductInfoLoad(driver):
    try:

        wait = WebDriverWait(driver, 15, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        elem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'head')))

        # elem = WebDriverWait(driver, 3).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'head'))


    except:
        print("Timeout while waiting for product info to load")

def ScrapAllInfo(driver):

    scrappedInfo= {}

    brandName = driver.find_element_by_tag_name('h1').get_attribute('innerHTML')
    medicineInfo = driver.find_element_by_class_name("medicine_info").find_elements_by_xpath("./child::*")
    saltInfo = None

    if len(medicineInfo) > 1:
        manufacName = medicineInfo[0].find_element_by_tag_name('a').get_attribute('innerHTML')
        saltInfo = medicineInfo[1].find_element_by_tag_name('b').get_attribute('innerHTML')
    else:
        manufacName = medicineInfo[0].find_element_by_tag_name('a').get_attribute('innerHTML')

    presciption = driver.find_element_by_xpath(prescriptionX)

    if(len(presciption.get_attribute('innerHTML')) <= 1):
        presciptionReq = False
    else:
        presciptionReq = True

    priceInfo = driver.find_element_by_xpath(priceInfoX).get_attribute('innerHTML')
    packSize = driver.find_element_by_xpath(packSizeX).get_attribute('innerHTML')

    # print(brandName)
    # print(manufacName)
    # print(saltInfo)
    # print(presciptionReq)
    # print(priceInfo)
    # print(packSize)

    scrappedInfo['Brand'] = brandName
    scrappedInfo['Manufacturer'] = manufacName
    scrappedInfo['Salt'] = saltInfo
    scrappedInfo['Presciption Required'] = presciptionReq
    scrappedInfo['Price'] = priceInfo
    scrappedInfo['Pack Size'] = packSize

    ############

    benefitsAndUses = []
    productUaB = driver.find_elements_by_xpath(productUaBX)
    if(len(productUaB) >= 1):
        for item in productUaB:
            try:
                benefitsAndUses.append(item.find_element_by_tag_name('a').get_attribute('innerHTML'))
            except :
                print("No a tag found in Benefits and uses list item") 

    # print(benefitsAndUses)
    
    scrappedInfo['Benefits and Uses'] = benefitsAndUses

    ############
    warnings = []
    productWarnings = driver.find_elements_by_xpath(productWarningsX)
    if(len(productWarnings) >= 1):
        for item in productWarnings:
            warnings.append(item.get_attribute('innerHTML'))


    # print(warnings)

    scrappedInfo['Warnings'] = warnings

    ################################

    contraindications = []
    productConIndics = driver.find_elements_by_xpath(productConIndicsX)
    if(len(productConIndics) >= 1 ):
        for item in productConIndics:
            contraindications.append(item.get_attribute('innerHTML'))

    # print(contraindications)

    scrappedInfo['ContraIndications'] = contraindications
    WriteInfoToCSV(scrappedInfo)

def readSaltInput():
    saltInput_raw = pd.read_excel('salts.xlsx')
    saltInput = saltInput_raw['Salt Name']
    return saltInput

def WriteInfoToCSV(scrappedData):
    with open('salt_scrapping.csv','a',encoding="utf-8") as file:
        for key in scrappedData:
            file.write(str(scrappedData[key]) + ';')
        file.write('\n')