from flask import Blueprint, render_template
from infrastructure.weather_api import OpenWeatherAPI
from domain.weather_service import WeatherService

router = Blueprint('router', __name__)

api_key = "SUA_API_KEY_AQUI"
weather_repository = OpenWeatherAPI(api_key)
weather_service = WeatherService(weather_repository)

@router.route("/")
def index():
    weather_info = weather_service.get_weather_with_forecast("Jaragua do Sul")
    print("DEBUG WEATHER RESPONSE:", weather_info)

    print("ROTA RECEBEU:", weather_info)


    return render_template("index.html", weather=weather_info)
