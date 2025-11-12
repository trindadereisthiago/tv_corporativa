from infrastructure.weather_api import OpenWeatherAPI
from domain.interfaces.weather_repository_interface import WeatherRepositoryInterface
from datetime import datetime

class WeatherService:
    def __init__(self, weather_repository: WeatherRepositoryInterface):
        self.weather_repository = weather_repository

    def get_weather_with_forecast(self, city_name: str):
        # --- 1) Dados do clima atual ---
        today_weather = self.weather_repository.get_today_weather(city_name)

        # --- 2) Previsão da semana ---
        week_weather = self.weather_repository.get_week_weather(city_name)
        if not week_weather:
            return {
                "current_temp": None,
                "current_description": None,
                "weekly_forecast": []
            }

        # --- 3) Temperatura e descrição atuais ---
        current_temp = None
        current_description = None
        if today_weather:
            current_temp = today_weather.get("main", {}).get("temp")
            if current_temp is not None:
                current_temp = int(round(current_temp))  # 🔥 remove casas decimais

            current_description = today_weather.get("weather", [{}])[0].get("description")

        # --- 4) Tradução dos dias da semana ---
        dias_pt = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        # --- 5) Montagem da previsão semanal ---
        weekly_forecast = []
        if "daily" in week_weather:
            for day in week_weather["daily"][:6]:
                date = datetime.strptime(day["date"], "%Y-%m-%d")
                weekday_en = date.strftime("%A")
                weekday = dias_pt.get(weekday_en, weekday_en)

                weekly_forecast.append({
                    "weekday": weekday,
                    "min": int(round(day["temp"].get("min", 0))),  # 🔥 arredondado sem casas decimais
                    "max": int(round(day["temp"].get("max", 0))),
                    "description": day["weather"][0].get("description", "").capitalize()
                })

        # --- 6) Retorno final ---
        return {
            "current_temp": current_temp,
            "current_description": current_description,
            "weekly_forecast": weekly_forecast
        }
