import requests

from app.core import settings


class GARService:
    def __init__(self):
        self.base_url = settings.gar.base_url
        self.user_agent = settings.gar.user_agent
        self._limit = 5
        self._format = "json"
        self._addressdetails = 1
        self._countrycodes = "ru"

    def fetch_gar_address(self, query):
        params = {
            "q": query,
            "format": self._format,
            "addressdetails": self._addressdetails,
            "limit": self._limit,
            "countrycodes": self._countrycodes
        }
        headers = {
            "User-Agent": self.user_agent
        }

        response = requests.get(self.base_url, params=params, headers=headers)
        return response.json()

    def fetch_gar_city(self, city):
        gar_city = ""
        if city:
            gar_city = self.fetch_gar_address(city)
            if gar_city:
                gar_city = gar_city[0].get("name")
        return gar_city
