import EnAPIAdapter
import time

LAT_LNG_LIST = [[40.128082,32.995083],[36.981944,35.280278],[36.916667,30.8],[40.248889,29.549444],[40.976111,28.814167],
                [38.289167,27.155],[38.770278,35.495278],[38.768889,34.526389],[37.456667,38.908056],[38.744722,41.653889]]

file_name_ten_day = "en-%s-10-day.csv" % time.strftime("%Y%m%d")
file_name_hourly = "en-%s-%s-hourly.csv" % (time.strftime("%Y%m%d"), time.strftime("%H-%M"))


def write_csv(csv_data, file_name):
    target = open(file_name, 'a+')
    target.write(csv_data)
    target.close()


def write_ten_day_csv(params):
    for i in LAT_LNG_LIST:
        csv_data = EnAPIAdapter.get_ten_day_forecast(i[0], i[1], "CSV", params)
        write_csv(csv_data, file_name_ten_day)


def write_hourly_csv(params):
    for i in LAT_LNG_LIST:
        csv_data = EnAPIAdapter.get_hourly_forecast(i[0], i[1], "CSV", params)
        write_csv(csv_data, file_name_hourly)


write_hourly_csv(None)
write_ten_day_csv(None)