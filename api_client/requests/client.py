import hashlib
from typing import List

import requests

from dto import Menu, Table, Hall, Restaurant


class JowiClient:
    BASE_URL: str = 'https://api.jowi.club/v010'
    API_KEY: str
    API_SECRET: str
    _session: requests.Session

    def __init__(self, api_key, api_secret, base_url=None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or self.BASE_URL

    @property
    def sig(self):
        full_sig = hashlib.sha256((self._api_key + self._api_secret).encode()).hexdigest()
        sig = full_sig[:10] + full_sig[-5:]
        return sig

    def __enter__(self):
        self._session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def list_restaurants(self) -> List[Restaurant]:
        url = f'{self._base_url}/restaurants?api_key={self._api_key}&sig={self.sig}'
        response = self._session.get(url)
        data = response.json()
        return Restaurant.from_jowi_response(data)

    def list_restaurant_menu(self, restaurant_id: str) -> Menu:
        url = f'{self._base_url}/restaurants/{restaurant_id}?api_key={self._api_key}&sig={self.sig}'
        response = self._session.get(url)
        data = response.json()
        return Menu.from_jowi_response(data)

    def list_restaurant_halls(self, restaurant_id: str) -> List[Hall]:
        url = f'{self._base_url}/halls?api_key={self._api_key}&sig={self.sig}&restaurant_id={restaurant_id}'
        response = self._session.get(url)
        data = response.json()
        return Hall.from_jowi_response(data)

    def list_hall_tables(self, hall_id: str, restaurant_id: str) -> List[Table]:
        url = f'{self._base_url}/halls/{hall_id}?api_key={self._api_key}&sig={self.sig}&restaurant_id={restaurant_id}'
        response = self._session.get(url)
        data = response.json()
        return Table.from_jowi_response(data)
