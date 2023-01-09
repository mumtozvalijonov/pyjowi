import hashlib
from typing import List

import requests
from pydantic import HttpUrl

from ...dto import CancelOrderDTO, CreateOrderDTO, Hall, Menu, Order, Restaurant, Table


class JowiClient:
    _session: requests.Session = None
    _api_key: str = None
    _api_secret: str = None
    _base_url: HttpUrl = "https://api.jowi.club"
    _sig: str = None

    def __init__(self, api_key: str, api_secret: str, base_url: HttpUrl = None):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url or self._base_url

    @property
    def signature(self):
        if not self._sig:
            full_sig = hashlib.sha256(
                (self._api_key + self._api_secret).encode()
            ).hexdigest()
            self._sig = full_sig[:10] + full_sig[-5:]
        return self._sig

    def __enter__(self):
        self._session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def list_restaurants(self) -> List[Restaurant]:
        url = f"{self._base_url}/v010/restaurants"
        params = {
            "api_key": self._api_key,
            "sig": self.signature,
        }
        response = self._session.get(url, params=params)
        data = response.json()
        return Restaurant.from_jowi_response(data)

    def list_restaurant_menu(self, restaurant_id: str) -> Menu:
        url = f"{self._base_url}/v010/restaurants/{restaurant_id}"
        params = {
            "api_key": self._api_key,
            "sig": self.signature,
        }
        response = self._session.get(url, params=params)
        data = response.json()
        return Menu.from_jowi_response(data)

    def list_restaurant_halls(self, restaurant_id: str) -> List[Hall]:
        url = f"{self._base_url}/v010/halls"
        params = {
            "api_key": self._api_key,
            "sig": self.signature,
            "restaurant_id": restaurant_id,
        }
        response = self._session.get(url, params=params)
        data = response.json()
        return Hall.from_jowi_response(data)

    def list_hall_tables(self, hall_id: str, restaurant_id: str) -> List[Table]:
        url = f"{self._base_url}/v010/halls/{hall_id}"
        params = {
            "api_key": self._api_key,
            "sig": self.signature,
            "restaurant_id": restaurant_id,
        }
        response = self._session.get(url, params=params)
        data = response.json()
        return Table.from_jowi_response(data)

    def create_order(self, order: CreateOrderDTO) -> Order:
        order.api_key = self._api_key
        order.signature = self.signature

        url = f"{self._base_url}/v3/orders"
        response = self._session.post(
            url,
            data=order.to_jowi_request(),
            headers={"Content-Type": "application/json"},
        )
        data = response.json()
        return Order.from_jowi_response(data)

    def get_order(self, order_id: str, restaurant_id: str) -> Order:
        url = f"{self._base_url}/v3/orders/{order_id}"
        params = {
            "api_key": self._api_key,
            "sig": self.signature,
            "restaurant_id": restaurant_id,
        }
        response = self._session.get(url, params=params)
        data = response.json()
        return Order.from_jowi_response(data)

    def cancel_order(self, cancellation: CancelOrderDTO) -> Order:
        cancellation.api_key = self._api_key
        cancellation.signature = self.signature

        url = f"{self._base_url}/v3/orders/{cancellation.order_id}/cancel"
        response = self._session.post(
            url,
            data=cancellation.to_jowi_request(),
            headers={"Content-Type": "application/json"},
        )
        data = response.json()
        return Order.from_jowi_response(data)
