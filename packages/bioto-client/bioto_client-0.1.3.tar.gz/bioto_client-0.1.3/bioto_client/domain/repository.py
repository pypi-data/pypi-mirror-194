from abc import ABC, abstractmethod
from pydantic import BaseModel
from requests import Response


class Garden(BaseModel):
    name: str


class Repository(ABC):
    @abstractmethod
    def get_gardens(self) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def search_garden(self, query: str) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def subscribe_garden(self, uuid: str) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self) -> None:
        raise NotImplementedError()
