# openweather.py
# 33
import os
import requests
from dotenv import load_dotenv

def get_local_weather(req_type):

    load_dotenv()
    OPENWEATHER_TOKEN = os.getenv('OPENWEATHER_TOKEN')

    def get_weather_forecast(api_key, city_name):
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"  # You can change units to "imperial" for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            return weather_data
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return None

    def get_weather_now(weather_data):
        weather_dict = {}
        if weather_data:
            city = weather_data["city"]["name"]
            index = 0
            for forecast in weather_data["list"]:
                if index == 0:
                    date_time = forecast["dt_txt"]
                    temperature = forecast["main"]["temp"]
                    description = forecast["weather"][0]["description"]
                    weather_dict[city] = f"{date_time}: {temperature}°C, {description}"
                    index += 1
                    #print(f"{date_time}: {temperature}°C, {description}")
        return weather_dict

    def get_forecast(weather_data):
        weather_dict = {}
        if weather_data:
            city = weather_data["city"]["name"]
            #print(f"Weather forecast for {city}:")

            for forecast in weather_data["list"]:
                date_time = forecast["dt_txt"]
                temperature = forecast["main"]["temp"]
                description = forecast["weather"][0]["description"]
                weather_dict[date_time] = f"{temperature}°C, {description}"
                #print(f"{date_time}: {temperature}°C, {description}")
        return weather_dict

    def display_weather_forecast(weather_data):
        if weather_data:
            city = weather_data["city"]["name"]
            print(f"Weather forecast for {city}:")

            for forecast in weather_data["list"]:
                date_time = forecast["dt_txt"]
                temperature = forecast["main"]["temp"]
                description = forecast["weather"][0]["description"]
                print(f"{date_time}: {temperature}°C, {description}")

    # Example usage:
    api_key = OPENWEATHER_TOKEN
    city_name = 'Ylöjärvi'  # Replace with the desired city
    weather_data = get_weather_forecast(api_key, city_name)
    #display_weather_forecast(weather_data)
    if req_type == "now":
        result = get_weather_now(weather_data)
    else:
        result = get_forecast(weather_data)
    return result
