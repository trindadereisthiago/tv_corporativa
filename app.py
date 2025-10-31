from domain.weather_service import WeatherService
from infrastructure.weather_api import OpenWeatherAPI

API_KEY = "7c6e17c43faf236d5cc939afab7dc5f3"

if __name__=="__main__":
    repo = OpenWeatherAPI(API_KEY)
    service = WeatherService(repo)

    result = service.get_weather("Jaraguá do Sul")
    print(result)