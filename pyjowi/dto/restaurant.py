from typing import List, Optional, Union

from pydantic import HttpUrl

from ._base import JowiResponseModel


class WorkingHours(JowiResponseModel):
    day: int
    start: str
    end: str
    is_day_off: bool

    @classmethod
    def _from_jowi_response_single(cls, response: dict) -> "WorkingHours":
        day = response.get("day_code")
        start = response.get("open_time")
        end = response.get("close_time")
        is_day_off = response.get("day_off")
        return cls(day=day, start=start, end=end, is_day_off=is_day_off)

    @classmethod
    def from_jowi_response(
        cls, response: dict
    ) -> Union[List["WorkingHours"], "WorkingHours"]:
        if isinstance(response, list):
            return [cls._from_jowi_response_single(item) for item in response]
        return cls._from_jowi_response_single(response)


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
    def from_jowi_response(cls, response: dict) -> List["Restaurant"]:
        data = response.get("restaurants")
        restaurants = []
        for restaurant_meta in data:
            phone_numbers = restaurant_meta.pop("phone_numbers")
            phone_numbers = phone_numbers.split(",") if phone_numbers else []

            working_hours = restaurant_meta.pop("work_timetable", [])
            working_hours = WorkingHours.from_jowi_response(working_hours)

            images = restaurant_meta.pop("images", [])
            images = [image.get("url") for image in images]

            restaurant = cls(
                phone_numbers=phone_numbers,
                work_timetable=working_hours,
                images=images,
                **restaurant_meta
            )
            restaurants.append(restaurant)
        return restaurants
