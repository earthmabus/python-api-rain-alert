import json
import requests
from twilio.rest import Client
import os

# keys needed for the application
OWM_API_KEY = os.environ.get("OPENWEATHERMAP_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

# my telephone number
MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")

# my current location
ORLANDO_LAT = 28.538336
ORLANDO_LONG = -81.379234

def load_current_weather_for_orlando():
    parameters = {'lat': ORLANDO_LAT, 'lon': ORLANDO_LONG, 'appid': OWM_API_KEY }
    response = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=parameters)
    response.raise_for_status()

    print(response.json())

def load_5day_forecast_weather_for_orlando():
    parameters = {'lat': ORLANDO_LAT, 'lon': ORLANDO_LONG, 'appid': OWM_API_KEY, 'cnt': 4 }
    print(parameters)
    response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
    response.raise_for_status()
    return response.json()

def bring_an_umbrella(weather_data):
    '''returns true if it will rain in your location in the next 12 hours according to the weather_data'''
    bring_umbrella = False
    for i in weather_data['list']:
        time = i['dt_txt']
        for j in i['weather']:
            id = j['id'] # 700
            main = j['main']
            description = j['description'] # light rain
            print(f"time: {time} , id: {id} , main: {main}")
            if id < 700:
                bring_umbrella = True
    return bring_umbrella

# grab the 5 day forecast and determine if it's going to rain in the next 12 hours today
weather_data = load_5day_forecast_weather_for_orlando()
will_rain_today = bring_an_umbrella(weather_data)

# if it's going to rain today, send an SMS to my phone
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
if will_rain_today:
    message = twilio_client.messages.create(to=MY_PHONE_NUMBER, from_="+18666196120",  body="hi michael, it's going to rain today!  remember to bring your umbrella")
    #print(f"{message.sid} - {message.status}")

# print(json.dumps(response.json(), indent=4))
