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

        jsondata = json.loads(data)["hourly_forecast"]
        for date in jsondata:
            print location + ', ' + date["FCTTIME"]["pretty"]
            print "Temperature: " + date["temp"]["metric"] + \
                " (ºC)".decode("utf-8")
            print "Condition: " + date["condition"]
            print "Wind speed: " + date["wspd"]["metric"] + " (Km/h)"
            print "Humidity: " + date["humidity"] + " (%)"
            print "Pressure: " + date["mslp"]["metric"] + " (hPa)" + '\n'

        return jsondata

    def almanac(self, location):
        """Saves 'almanac' data."""
        data = self.requestData("almanac")

        jsondata = json.loads(data)
        almanac = jsondata["almanac"]  # all the data

        useful_data = {}  # just useful data for us
        useful_data["max"] = {}
        useful_data["min"] = {}
        useful_data["max"]["avg"] = almanac["temp_high"]["avg"]["C"]
        useful_data["ma"]["record"] = almanac["temp_high"]["record"]["C"]
        useful_data["min"]["avg"] = almanac["temp_low"]["avg"]["C"]
        useful_data["min"]["record"] = almanac["temp_low"]["record"]["C"]

        print_almanac(useful_data)


def print_almanac(useful_data):
    """Prints saved data as a dict"""
    print "High Temperatures:"
    print "Average on this date", useful_data["high"]["normal"]
    print "Record on this date %s (%s) " % \
        (useful_data["high"]["record"],
            useful_data["high"]["year"])
    print "Low Temperatures:"
    print "Average on this date", useful_data["low"]["normal"]
    print "Record on this date %s (%s) " % \
        (useful_data["low"]["record"],
            useful_data["low"]["year"])


if __name__ == "__main__":
    if not api_key:
        try:
            api_key = sys.argv[1]
        except IndexError:
            key_file = open('api_key', 'r')
            api_key = key_file.read().replace('\n', '')
            print "Must provide api key in code or cmdline arg"

    weatherclient = WeatherClient(api_key)
#  print_almanac(weatherclient.almanac(location))
