from typing import Optional, List

from pydantic import HttpUrl

from ._base import JowiResponseModel


class WorkingHours(JowiResponseModel):
    day: str
    start: str
    end: str
    is_day_off: bool


class Restaurant(JowiResponseModel):
    id: str
    title: str
    phone_numbers: List[str]
    website: Optional[str]
    restaurant_type: Optional[str]
    address: Optional[str]
    latitude: float
    longitude: float
    country: str
    city: Optional[str]
    is_online_order_enabled: bool = False
    is_online_reserve_enabled: bool = False
    work_timetable: List[WorkingHours]
    images: List[HttpUrl]

    @classmethod
    def from_jowi_response(cls, response: dict) -> List['Restaurant']:
        data = response.get('restaurants')
        restaurants = []
        for restaurant_meta in data:
            phone_numbers = restaurant_meta.pop('phone_numbers')
            phone_numbers = phone_numbers.split(',') if phone_numbers else []
            restaurant = cls(
                phone_numbers=phone_numbers,
                **restaurant_meta
            )
            restaurants.append(restaurant)
        return restaurants
