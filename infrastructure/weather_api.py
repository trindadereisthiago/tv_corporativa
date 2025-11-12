import requests
from domain.interfaces.weather_repository_interface import WeatherRepositoryInterface
from collections import defaultdict, Counter

class OpenWeatherAPI(WeatherRepositoryInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_today_weather(self, city: str):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=pt_br"
        response = requests.get(url, verify=False)
        return response.json()

    def get_week_weather(self, city: str):
        # 1) Buscar previsão 5 dias (3h intervalos)
        url = f"https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br"
        }

        data = requests.get(url, params=params, verify=False).json()

        # se a API retornar erro
        if "list" not in data:
            print("Erro ao buscar previsão semanal:", data)
            return None

        # 2) Agregar por dia
        daily = defaultdict(lambda: {"min": 999, "max": -999, "weather": []})

        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            temp = item["main"]["temp"]
            desc = item["weather"][0]["description"]

            daily[date]["min"] = min(daily[date]["min"], temp)
            daily[date]["max"] = max(daily[date]["max"], temp)
            daily[date]["weather"].append(desc)

        # 3) Converter no formato parecido com OneCall (compatível com seu serviço)
        formatted = {"daily": []}
        for date, val in list(daily.items())[:7]:  # primeiros 7 dias
            most_common_desc = Counter(val["weather"]).most_common(1)[0][0]
            formatted["daily"].append({
                "date": date,  # <<--- ADD AQUI
                "temp": {
                    "min": int(round(val["min"])),
                    "max": int(round(val["max"]))
                },
                "weather": [{"description": most_common_desc}]
            })

        return formatted
