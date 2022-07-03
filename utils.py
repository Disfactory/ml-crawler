from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def screenShot(url, filename):
    options = Options()
    options.binary_location = "/usr/bin/brave-browser"

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    driver.get(url)
    # maximize browser

    driver.maximize_window()
    sleep(3)

    option = driver.find_element(By.CLASS_NAME, value="reference-layer-toggle")
    child = option.find_element(By.TAG_NAME, "svg")

    child.click()
    sleep(3)

    driver.get_screenshot_as_file(filename)
    driver.quit()


if __name__ == "__main__":
    # source id list
    source_id_dict = {
        2014: 10,
        2017: 31026,
        2019: 11351,
        2020: 9181,
        2021: 15423,
    }

    lat, lon = 23.94087, 120.64671
    lat_diff = 0.00689
    lon_diff = 0.01169
    year = 2020  # available years: 2014, 2017, 2019, 2020, 2021

    source_id = source_id_dict[year]
    url = f"https://livingatlas.arcgis.com/wayback/#active={source_id}&ext={lon},{lat},{lon + lon_diff},{lat + lat_diff}&localChangesOnly=true"
    filename = "screenshot.png"
    screenShot(url, filename)
