import EnAPIAdapter
import time
import csv


file_name_ten_day = "en-%s-10-day.csv" % time.strftime("%Y%m%d")
file_name_hourly = "en-%s-%s-hourly.csv" % (time.strftime("%Y%m%d"), time.strftime("%H-%M"))


def read_lat_and_lng():
    lat_lng_dict = {"names":[],"lats":[],"lngs":[]}
    path = open("locations.csv","r+")
    reader = csv.reader(path,delimiter=";")
    for row in reader:
        lat_lng_dict["names"].append(row[0])
        lat_lng_dict["lats"].append(row[1])
        lat_lng_dict["lngs"].append(row[2])
    return lat_lng_dict


def write_csv(csv_data, file_name):
    target = open(file_name, 'a+')
    target.write(csv_data)
    target.close()


def write_ten_day_csv(params):
    lat_lng_dict = read_lat_and_lng()
    for i in range(len(lat_lng_dict["lats"])):
        csv_data = EnAPIAdapter.get_ten_day_forecast(lat_lng_dict["lats"][i], lat_lng_dict["lngs"][i], "CSV", params)
        write_csv(csv_data, file_name_ten_day)


def write_hourly_csv(params):
    lat_lng_dict = read_lat_and_lng()
    for i in range(len(lat_lng_dict["lats"])):
        csv_data = EnAPIAdapter.get_hourly_forecast(lat_lng_dict["lats"][i], lat_lng_dict["lngs"][i], "CSV", params)
        write_csv(csv_data, file_name_hourly)


write_ten_day_csv(None)
write_hourly_csv(None)