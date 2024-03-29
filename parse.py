# import xlrd
import openpyxl
import pickle

from utils import screenShot


if __name__ == '__main__':
    restart = False

    if restart:
        xlsx_file = openpyxl.load_workbook('data/full-data.xlsx')
        sheet = xlsx_file['2022full-info']
        f = open('data/full-info.pickle', 'wb')
        pickle.dump(sheet, f)
        f.close()
    else:
        f = open('data/full-info.pickle', 'rb')
        sheet = pickle.load(f)
        f.close()

    year_list = [2017, 2020]

    num_locations = 10 # in total 53319
    for row_id, row in enumerate(sheet.iter_rows(max_row=num_locations)):
        if row_id == 0:
            continue
        # lon,  lat   = float(row[0].value),  float(row[1].value)
        lon_min, lon_max = float(row[2].value), float(row[4].value)
        lat_min, lat_max = float(row[3].value), float(row[5].value)

        lon = (lon_min + lon_max) / 2
        lat = (lat_min + lat_max) / 2

        size, price = float(row[13].value), float(row[17].value)
        # print(row_id, lon, lat, size, price)

        for year in year_list:
            screenShot(row_id, lat, lon, year)
            # screenShot(row_id, lat_min, lat_max, lon_min, lon_max, year)


