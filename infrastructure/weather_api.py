import requests

class OpenWeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={self.api_key}&q={city}"
        response = requests.get(url)
        return response.json()