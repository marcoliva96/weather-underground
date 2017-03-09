#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :

import sys
import json
import requests

api_key = None

location = 'Lleida'
response_format = '.json'


class WeatherClient(object):
    """Access wunderground and collects data via API"""

    url_base = "http://api.wunderground.com/api/"
    url_services = {
        "almanac": "/almanac/q/CA/",
        "hourly": "/hourly/q/CA/"
    }

    def __init__(self, api_key):
        super(WeatherClient, self).__init__()
        self.api_key = api_key

    def requestData(self, url_service_name):
        """Downloads web data using requests."""
        url = self.url_base + self.api_key + \
            self.url_services[url_service_name] + \
            location + response_format

        return requests.get(url).text

    def hourly(self, location):
        """Saves 'hourly' data."""
        data = self.requestData("hourly")
        jsondata = json.loads(data)["hourly_forecast"]  # all the data

        useful_data = []  # just useful data for us
        hourly_data = {}
        for hour in jsondata:
                hourly_data["location"] = hour["FCTTIME"]["pretty"]
                hourly_data["temp"] = hour["temp"]["metric"]
                hourly_data["condition"] = hour["condition"]
                hourly_data["wind"] = hour["wspd"]["metric"]
                hourly_data["humidity"] = hour["humidity"]
                hourly_data["pressure"] = hour["mslp"]["metric"]
                useful_data.append(hourly_data.copy())
        return useful_data

    def almanac(self, location):
        """Saves 'almanac' data."""
        data = self.requestData("almanac")
        jsondata = json.loads(data)["almanac"]  # all the data

        useful_data = {}  # just useful data for us
        useful_data["max"] = {}
        useful_data["min"] = {}
        useful_data["max"]["avg"] = jsondata["temp_high"]["normal"]["C"]
        useful_data["max"]["record"] = jsondata["temp_high"]["record"]["C"]
        useful_data["min"]["avg"] = jsondata["temp_low"]["normal"]["C"]
        useful_data["min"]["record"] = jsondata["temp_low"]["record"]["C"]

        return useful_data


def print_almanac(useful_data):
    """Prints saved data as a dict"""
    #  {'max': {'record': u'21', 'avg': u'16'},
    #  'min': {'record': u'-1', 'avg': u'6'}}
    print "Past years temperature data on this date:"
    print "(Highest ever", useful_data["max"]["record"] + ")"
    print "High average", useful_data["max"]["avg"]
    print "Low average", useful_data["min"]["avg"]
    print "(Lowest ever", useful_data["min"]["record"] + ")" + '\n'


def print_hourly(useful_data):
    """Prints saved data as a dict"""
    for hourly_data in useful_data:
        print location + ', ' + hourly_data["location"]
        print "Temperature: " + hourly_data["temp"] + \
            " (ºC)".decode("utf-8")
        print "Condition: " + hourly_data["condition"]
        print "Wind speed: " + hourly_data["wind"] + " (Km/h)"
        print "Humidity: " + hourly_data["humidity"] + " (%)"
        print "Pressure: " + hourly_data["pressure"] + " (hPa)" + '\n'


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            key_file = open('api_key', 'r')
            api_key = key_file.read().replace('\n', '')
            print "Must provide api key in code or cmdline arg"

    weatherclient = WeatherClient(api_key)
print_almanac(weatherclient.almanac(location))
print_hourly(weatherclient.hourly(location))
