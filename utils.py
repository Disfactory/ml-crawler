from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PIL import Image

import datetime
import ee
import folium
from matplotlib import pyplot as plt

ee.Initialize()

# source id list
source_id_dict = {
    # 2014: 10,
    2017: 14035,
    # 2019: 11351,
    2020: 18289,
    # 2021: 15423,
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

    im = Image.open(folder_path + filename)
    width, height = im.size
    print('width {}, height {}'.format(width, height))

    center = width / 5 * 3
    crop_width = 224 # width / 10
    left   = center - crop_width / 2
    right  = center + crop_width / 2

    middle = height / 2
    crop_height = 224 # height / 8
    top    = middle - crop_height / 2
    bottom = middle + crop_height / 2

    im1 = im.crop((left, top, right, bottom))
    # im1.show()
    im1.save(folder_path + filename)
    # im1.close()

# def add_ee_layer(self, ee_image_object, vis_params, name):
#     map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
#     folium.raster_layers.TileLayer(
#         tiles=map_id_dict['tile_fetcher'].url_format,
#         attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
#         name=name,
#         overlay=True,
#         control=True
#     ).add_to(self)
# 
# folium.Map.add_ee_layer = add_ee_layer


# landsat surface reflection
# def get_ee_landsat(filename, region, scale=30):
#     def maskL8sr(image):
#       #  Bits 3 and 5 are cloud shadow and cloud, respectively.
#       cloudShadowBitMask = (1 << 3)
#       cloudsBitMask = (1 << 5)
#       #  Get the pixel QA band.
#       qa = image.select('pixel_qa')
#       # Both flags should be set to zero, indicating clear conditions.
#       mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0) and (qa.bitwiseAnd(cloudsBitMask).eq(0))
#       return image.updateMask(mask)
# 
#     landsat    = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterDate('2020-01-01', '2020-12-31').filterBounds(region).map(maskL8sr).select(['B4', 'B3', 'B2'])
# 
#     task = ee.batch.Export.image.toDrive(image=landsat.mean(),  # an ee.Image object.
#                                          region=region, # an ee.Geometry object.
#                                          folder='human-wildlife-conflict',
#                                          fileNamePrefix=filename,
#                                          scale=scale)


# Sentinel-2
def get_ee_s2(filename, region, scale=30):
    # mask for Sentinel-2
    def maskS2clouds(image):
      qa = image.select('QA60')
      # Bits 10 and 11 are clouds and cirrus, respectively.
      cloudBitMask = 1 << 10
      cirrusBitMask = 1 << 11
      # Both flags should be set to zero, indicating clear conditions.
      mask = qa.bitwiseAnd(cloudBitMask).eq(0) and qa.bitwiseAnd(cirrusBitMask).eq(0)
      return image.updateMask(mask).divide(10000)

    s2Sr       = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterDate('2020-01-01', '2020-01-31').filterBounds(region).map(maskS2clouds) #.select(['B4', 'B3', 'B2'])
    # s2Cloud    = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY').filterDate('2020-01-01', '2020-01-31').filterBounds(region).map

    task = ee.batch.Export.image.toDrive(image=s2Sr.mean(),  # an ee.Image object.
                                         region=region, # an ee.Geometry object.
                                         folder='disfactory',
                                         fileNamePrefix=filename,
                                         scale=scale)
    task.start()
    return task


if __name__ == '__main__':
    # scale: the scale of the imagery (meter per pixel)
    # center: (latitude, longitude)
    # radius: in degree of longitude, latitude. 1 degree ~ 111km

    # lat, lon = 23.94087, 120.64671
    # year = 2020 # available years: 2014, 2017, 2019, 2020, 2021
    # 
    # source_id = source_id_dict[year]
    # screenShot(0, lat, lon, year)

    center = (17.7009, 83.277) # lat, long
    radius = 0.1
    region = ee.Geometry.Rectangle([center[1]-radius, center[0]-radius, center[1]+radius, center[0]+radius])

    filename = 'new'
    task = get_ee_s2(filename, region)

