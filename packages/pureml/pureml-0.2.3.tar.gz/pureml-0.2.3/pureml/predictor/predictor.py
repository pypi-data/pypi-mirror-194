from pydantic import BaseModel, Field
import typing
from typing import List, Any
from abc import ABC, abstractmethod

from enum import Enum


# class ModelDetails(str, Enum):
#     name = ""
#     branch = ""
#     version = ""


class BasePredictor(BaseModel, ABC):
    # model_details: typing.Union[typing.List["str"], typing.List[typing.List["str"]]]
    # model_details: typing.Union[ModelDetails, typing.List[ModelDetails]]
    model_details: list
    model: Any = None
    requirements_py: list = None
    requirements_sys: list = None

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def predict(self, **kwargs: typing.Any):
        pass

    # @abstractmethod
    def load_requirements_py(self):
        pass

    # @abstractmethod
    def load_requirements_sys(self):
        pass

    @abstractmethod
    def load_models(self):
        pass

    # @abstractmethod
    def load_resources(self):
        pass
