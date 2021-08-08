from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from variables import * 
import functions as f


# global driver
driver = webdriver.Firefox(executable_path=pathToFireforDriver)


queryList = f.readSaltInput()    

global resultsCount

def iterateOverQueryItem():
    for cQuery in queryList:
        print("Fetching data for " + str(cQuery))
        try:
            main(cQuery)
        except:
            print("Could not fetch anything for " + str(cQuery))


def main(currentQuery):

    url = 'https://www.myupchar.com/en/medicines_list?query=' + str(currentQuery)
    driver.get(url)

    f.waitForParentContainerLoad(driver)

    resultsCount = f.findNoOfResultsInPage(driver) 
    i = 1
    page = 1

    while i <= resultsCount :

        f.waitForChildContainerLoad(driver,i)
        f.removeSiteObstructions(driver)
        container = driver.find_element_by_xpath('//div[@class="col-md-6"][' + str(i) + ']/a')
        container.click()
        print("Fetching data for :" + str(currentQuery) + "item no : " +str(i) + " in page :" + str(page))
        f.waitForProductInfoLoad(driver)
        ##Scrap Data Here ===
        f.ScrapAllInfo(driver)
        driver.get('https://www.myupchar.com/en/medicines_list?page='+ str(page) + '&query=' + currentQuery)
        f.waitForChildContainerLoad(driver,i)


        if i == resultsCount:
            try:
                nextBtn = driver.find_element_by_xpath('//a[@aria-label="Next"]')
                driver.get(nextBtn.get_attribute('href'))
                f.waitForParentContainerLoad(driver)
                # driver.implicitly_wait(5) 
                resultsCount = f.findNoOfResultsInPage(driver)
                page = page + 1
                i = 1
                continue

            except:
                print("No next page found...")
                break
        else:
            i += 1

iterateOverQueryItem()