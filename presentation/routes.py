from flask import Blueprint, render_template
from infrastructure.weather_api import OpenWeatherAPI
from domain.weather_service import WeatherService
from dotenv import load_dotenv
import os

router = Blueprint('router', __name__)

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
weather_repository = OpenWeatherAPI(api_key)
weather_service = WeatherService(weather_repository)

@router.route("/")
def index():
    weather_info = weather_service.get_weather_with_forecast("Jaragua do Sul")
    print("DEBUG WEATHER RESPONSE:", weather_info)

    print("ROTA RECEBEU:", weather_info)


    return render_template("index.html", weather=weather_info)
