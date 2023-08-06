from pydantic import BaseModel, root_validator
from .singleton import Singleton_BaseModel
import typing
import os


class BackendSchema(Singleton_BaseModel):

    BASE_URL: str = "https://pureml-development.up.railway.app/api/"

    class Config:
        arbitrary_types_allowed = True
