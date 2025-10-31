from abc import ABC, abstractmethod

class WeatherRepositoryInterface(ABC):

    @abstractmethod
    def get_today_weather(self, city: str):
        pass

    @abstractmethod
    def get_week_weather(self, city: str):
        pass
