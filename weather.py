import requests
import os

WEATHER_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city="Tirunelveli"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
    return requests.get(url).json()
