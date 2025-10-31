from domain.weather_service import WeatherService

class FakeWeatherRepository:
    def get_weather(self, city_name: str):
        return {"temp": 25, "condition": "Clear"}

def test_weather_service_init():
    fake_repo = FakeWeatherRepository()
    service = WeatherService(fake_repo)
    assert service is not None
