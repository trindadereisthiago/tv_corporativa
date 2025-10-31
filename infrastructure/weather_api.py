import requests
from domain.interfaces.weather_repository_interface import WeatherRepositoryInterface

class OpenWeatherAPI(WeatherRepositoryInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_today_weather(self, city: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=pt_br"
        response = requests.get(url, verify=False)
        return response.json()

    def get_week_weather(self, city: str):
        # 1) pegar latitude e longitude
        url_geo = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&appid={self.api_key}"
        geo = requests.get(url_geo, verify=False).json()

        if not geo or isinstance(geo, dict):
            print("Erro.")
            return None
        
        lat = geo[0]["lat"]
        lon = geo[0]["lon"]

        # 2) Previsão estendida
        url_week = (
            f"https://api.openweathermap.org/data/3.0/onecall?"
            f"lat={lat}&lon={lon}&appid={self.api_key}&units=metric&exclude=hourly,minutely&lang=pt_br"
        )

        week = requests.get(url_week, verify=False).json()
        return week
