from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# source id list
source_id_dict = {
    2014: 10,
    2017: 31026,
    2019: 11351,
    2020: 9181,
    2021: 15423,
    }

def screenShot(location_id, lat, lon, year):
    lat_diff = 0.00689
    lon_diff = 0.01169
    folder_path = 'data/images/'

    source_id = source_id_dict[year]
    lon_min, lon_max = lon - lon_diff/2, lon + lon_diff/2
    lat_min, lat_max = lat - lat_diff/2, lat + lat_diff/2

    url = 'https://livingatlas.arcgis.com/wayback/#active={}&ext={},{},{},{}&localChangesOnly=true'.format(source_id, lon_min, lat_min, lon_max, lat_max)
    print(url)
    filename = 'location{}_year{}.png'.format(location_id, year)

    driver = webdriver.Chrome(executable_path='drivers/linux/chromedriver') # Linux
    # driver = webdriver.Chrome(executable_path='drivers/macos/chromedriver') # Mac

    driver.get(url)
    #maximize browser
    driver.maximize_window()
    sleep(3)

    option = driver.find_element(By.CLASS_NAME, value='reference-layer-toggle')
    child = option.find_element(By.TAG_NAME, 'svg')

    child.click()
    sleep(3)

    driver.get_screenshot_as_file(folder_path + filename)
    driver.quit()

if __name__ == '__main__':
    lat, lon = 23.94087, 120.64671
    year = 2020 # available years: 2014, 2017, 2019, 2020, 2021

    source_id = source_id_dict[year]
    screenShot(0, lat, lon, year)

