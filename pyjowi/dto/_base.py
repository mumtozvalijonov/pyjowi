import abc
from typing import Union, List

from pydantic import BaseModel


class JowiResponseModel(BaseModel, abc.ABC):

    @classmethod
    @abc.abstractmethod
    def from_jowi_response(cls, response: dict) -> Union['JowiResponseModel', List['JowiResponseModel']]:
        return cls(**response)


class JowiRequestModel(BaseModel, abc.ABC):

    @abc.abstractmethod
    def to_jowi_request(self) -> dict:
        return self.dict()
