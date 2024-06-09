import requests
import json
import math
from dotenv import load_dotenv
import os


# Access the API key from the environment variable
load_dotenv()
weather_api_key = os.getenv("API_KEY")

# Set the city name
city_name='East Lansing'

def get_weather(weather_api_key, city_name):

    # Set URL for API
    url='https://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=2&aqi=yes&alerts=yes' % (weather_api_key, city_name)
   
    # Get data from API
    response = requests.get(url)
    data = response.json()

    return data

def get_weather_data(data):
    #from the sample json data extract the following information
    #current day and time
    #forecast data

def wbgt_estimator(temp,humidity):

    #calculate the vapor pressure
    vapor_pressure = humidity/100 * 6.105 * math.exp(17.27*temp/(237.7+temp))

    #calculate the WBGT index using the Gagge and Nishi formula
    wbgt = 0.567*temp + 0.393*vapor_pressure + 3.94

    #return the WBGT index
    return wbgt

def performance_loss_calculator(wbgt):

    #estimate performance loss based on regression of Ely et al. (2007)
    performance_loss = 1.2671*math.exp(0.3198*wbgt)
    
    return performance_loss

def mph_to_min_per_mile(mph):
    if mph <= 0:
        raise ValueError("Speed must be positive")

    min_per_mile = 60 / mph
    minutes = int(min_per_mile)
    seconds = int((min_per_mile * 60) % 60)
    
    return minutes, seconds

def min_per_mile_to_mph(minutes, seconds):
    if minutes < 0 or seconds < 0 or seconds >= 60:
        raise ValueError("Invalid time format")
    
    total_minutes = minutes + seconds / 60
    mph = 60 / total_minutes
    
    return mph

def adjust_pace(pace_str, performance_loss_percentage):
    try:
        pace_minutes, pace_seconds = map(int, pace_str.split(':'))
    except ValueError:
        raise ValueError("Invalid pace format. Please use mm:ss format")

    if pace_minutes < 0 or pace_seconds < 0 or pace_seconds >= 60:
        raise ValueError("Invalid time format")
    if performance_loss_percentage < 0 or performance_loss_percentage >= 100:
        raise ValueError("Percentage decrease should be between 0 and 100")

    total_pace_seconds = pace_minutes * 60 + pace_seconds
    adjusted_pace_seconds = total_pace_seconds * (1 - performance_loss_percentage / 100)
    adjusted_pace_minutes = adjusted_pace_seconds // 60
    adjusted_pace_seconds %= 60

    return f"{int(adjusted_pace_minutes):02d}:{int(adjusted_pace_seconds):02d}"
