import abc
from typing import Union, List

from pydantic import BaseModel


class JowiBaseModel(BaseModel, abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_jowi_response(cls, response: dict) -> Union['JowiBaseModel', List['JowiBaseModel']]:
        return cls(**response)
