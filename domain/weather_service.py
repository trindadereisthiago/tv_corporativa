class WeatherService:
    def __init__(self, weather_repository):
        self.weather_repository = weather_repository

    def get_weather(self, city):
        #chama quem realmente coleta (infra)
        data = self.weather_repository.get_weather(city)

    #regra de negocio simples
        return {
            "city": city,
            "condition": data["weather"][0]["main"],
            "temperature": round(data["main"]["temp"] - 273.15, 1)
        }