import json
import requests
from pprint import pprint


class Weather:
    """
    Creates a Weather object getting an apikey as input and 
    either a city name or latitude and longitude coorditates.
    """

    def __init__(self, api, units=None, city=None, lat=None, long=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api}&units={units}"
            r = requests.get(url)
            self.data = r.json()
        elif lat and long:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={api}&units={units}"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Write city or latitude and longitude for a place")

        if self.data['cod'] != "200":
            raise ValueError(self.data["message"])

    def next_12(self):
        """
        Returns 3-hour data for the next 12 hours as a dict.
        """
        return self.data["list"][:4]

    def next_12_simplified(self):
        """
        Returns the date, temperature, and sky condition every 3 hours 
        for the next 12 hours as a tuple of tuples
        """
        simple_data = []
        for dicty in self.data["list"][:4]:
            simple_data.append((dicty["dt_txt"], dicty["main"]["temp_max"],
                               dicty["weather"][0]["description"]))
        return simple_data
