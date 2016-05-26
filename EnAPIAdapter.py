import json
import urllib2

global TOKEN
TOKEN = ""

BASE_URL_GOOGLE = "http://maps.google.com/maps/api/geocode/json?address="
TOKEN_BASE_URL = "https://thepulseapi.earthnetworks.com/oauth20/token?grant_type=client_credentials&client_id="
CLIENT_ID = "9ac974dff4db410d913a6bc261fb061b"
CLIENT_SECRET = "beca86f5668a49228086dda66a1f5d5a"
TEN_DAY_BASE_URL = "https://thepulseapi.earthnetworks.com/data/forecasts/v1/daily?location="
HOURLY_BASE_URL = "https://thepulseapi.earthnetworks.com/getHourly6DayForecast/data/forecasts/v1/hourly?location="

DEFAULT_HOURLY_PARAMS = ["forecastDateUtcStr", "cloudCoverPercent", "description", "dewPoint", "feelsLike",
                         "forecastDateLocalStr", "adjustedPrecipProbability", "iconCode", "precipCode", "precipProbability",
                         "precipRate", "relativeHumidity", "temperature", "thunderstormProbability", "windDirectionDegrees",
                         "windSpeed", "surfacePressure", "snowRate", "globeTemperature", "wetBulbTemperature"]

DEFAULT_TEN_DAY_PARAMS = ["forecastDateUtcStr", "dewPoint", "iconCode", "precipCode", "precipProbability", "relativeHumidity",
                          "summaryDescription", "temperature", "thunderstormProbability", "windDirectionDegrees", "windSpeed",
                          "snowAmountMm", "detailedDescription", "forecastDateLocalStr", "cloudCoverPercent", "isNightTimePeriod"]


def set_token(arg):
    global TOKEN
    TOKEN = arg


def get_json_data(final_url):
    my_final_url = final_url + str(TOKEN)
    try:
        response = urllib2.urlopen(my_final_url)
    except urllib2.HTTPError:
        set_token(return_token())
        my_final_url = final_url + str(TOKEN)
        response = urllib2.urlopen(my_final_url)

    json_data = json.load(response)
    return json_data


def get_ten_day_forecast(lat, lng, return_format, params=None):
    final_url = TEN_DAY_BASE_URL + str(lat) + "," + str(lng) + \
        "&locationtype=latitudelongitude&units=metric&cultureinfo=en-en&verbose=true&access_token="

    json_data = get_json_data(final_url)

    if return_format == "JSON":
        return json_data
    elif return_format == "CSV":
        if params is None:
            params = DEFAULT_TEN_DAY_PARAMS
        return convert_to_csv_ten_day(lat, lng, json_data, params)


def get_hourly_forecast(lat, lng, return_format, params=None):
    final_url = HOURLY_BASE_URL + str(lat) + "," + str(lng) + \
        "&locationtype=latitudelongitude&units=english&cultureinfo=en-en&verbose=true&access_token="

    json_data = get_json_data(final_url)

    if return_format == "JSON":
        return json_data
    elif return_format == "CSV":
        if params is None:
            params = DEFAULT_HOURLY_PARAMS
        return convert_to_csv_hourly(lat, lng, json_data, params)


def return_token():
    final_url = TOKEN_BASE_URL + CLIENT_ID + "&client_secret=" + CLIENT_SECRET
    response = urllib2.urlopen(final_url)
    json_data = json.load(response)
    token = json_data["OAuth20"]["access_token"]["token"]
    refresh_token = json_data["OAuth20"]["access_token"]["refresh_token"]
    if token != refresh_token:
        return return_token()

    return token


def convert_to_csv_ten_day(lat, lng, json_data, params):
    json_data = json_data["dailyForecastPeriods"]
    csv_string = ""

    for p in json_data:
        for count in range(len(params)):
            csv_string += str(p[params[count]]) + ";"
        csv_string += "%s;%s" % (str(lat), str(lng))
        csv_string += "\n"

    return csv_string


def convert_to_csv_hourly(lat, lng, json_data, params):
    json_data = json_data["hourlyForecastPeriod"]
    csv_string = ""

    for row in json_data:
        for p in range(len(params)):
            csv_string += str(row[params[p]]) + ";"
        csv_string += "%s;%s" % (str(lat), str(lng))
        csv_string += "\n"

    return csv_string
