from typing import List, Optional

from pydantic import HttpUrl, validator

from ._base import JowiResponseModel


class MenuCategoryCourse(JowiResponseModel):
    id: str
    title: str
    price: float
    price_for_online_order: float
    is_exception: bool
    is_online_order: bool
    is_vegetarian: Optional[bool]
    description: Optional[str]
    image_url: Optional[HttpUrl]
    count_left: Optional[int]

    @classmethod
    def from_jowi_response(cls, response: dict) -> "MenuCategoryCourse":
        is_online_order = response.pop("online_order", False)
        return cls(is_online_order=is_online_order, **response)

    @validator("count_left", pre=True)
    def validate_count_left(cls, v):
        if v is None:
            return 0
        elif isinstance(v, str):
            return int(float(v))
        return v


class MenuCategory(JowiResponseModel):
    title: str
    courses: List[MenuCategoryCourse]

    @classmethod
    def from_jowi_response(cls, response: dict) -> "MenuCategory":
        courses_meta = response.get("courses", [])
        courses = [
            MenuCategoryCourse.from_jowi_response(course_meta)
            for course_meta in courses_meta
        ]
        return cls(title=response["title"], courses=courses)


class Menu(JowiResponseModel):
    categories: List[MenuCategory]

    @classmethod
    def from_jowi_response(cls, response: dict) -> "Menu":
        category_metas = response.get("categories", [])
        categories = [
            MenuCategory.from_jowi_response(category_meta)
            for category_meta in category_metas
        ]
        return cls(categories=categories)
