from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def screenShot(url, filename):
    # driver = webdriver.Chrome(executable_path='drivers/linux/chromedriver') # Linux
    driver = webdriver.Chrome(executable_path='drivers/macos/chromedriver') # Mac

    driver.get(url)
    #maximize browser
    driver.maximize_window()
    sleep(3)

    # option = driver.find_element_by_class_name('reference-layer-toggle')
    option = driver.find_element_by_xpath("//button")

    print("Value is: %s" % option.get_attribute("value"))
    option.click()
    sleep(3)

    driver.get_screenshot_as_file(filename)
    driver.quit()
    print("end...")

if __name__ == '__main__':
    url = 'https://livingatlas.arcgis.com/wayback/#active=9181&ext=120.54671,23.84087,120.55840,23.84776&localChangesOnly=true'
    filename = 'screenshot.png'
    screenShot(url, filename)

    
