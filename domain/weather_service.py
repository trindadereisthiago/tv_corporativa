from infrastructure.weather_api import OpenWeatherAPI
from domain.interfaces.weather_repository_interface import WeatherRepositoryInterface

class WeatherService:
    def __init__(self, weather_repository):
        self.weather_repository = weather_repository

    def get_weather_with_forecast(self, city_name: str):
        # dados do clima atual
        today_weather = self.weather_repository.get_today_weather(city_name)

        # previsão da semana
        week_weather = self.weather_repository.get_week_weather(city_name)
        if not week_weather:
            return {
        "current_temp": None,
        "current_description": None,
        "weekly_forecast": []
        }

        # debug temporário
        print("=== DADOS HOJE ===")
        print(today_weather)

        print("\n=== DADOS SEMANA ===")
        print(week_weather)

        # extrair temp atual
        current_temp = today_weather.get("main", {}).get("temp") if today_weather else None
        current_description = today_weather.get("weather", [{}])[0].get("description") if today_weather else None

        # extrair previsões dos próximos dias
        weekly_forecast = []
        if week_weather and "daily" in week_weather:
            for day in week_weather["daily"][:7]:  # só 7 dias
                weekly_forecast.append({
                    "min": day["temp"].get("min"),
                    "max": day["temp"].get("max"),
                    "description": day["weather"][0].get("description")
                })

        return {
            "current_temp": current_temp,
            "current_description": current_description,
            "weekly_forecast": weekly_forecast
        }
