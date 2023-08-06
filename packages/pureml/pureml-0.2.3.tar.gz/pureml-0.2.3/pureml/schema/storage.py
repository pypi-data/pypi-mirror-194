from pydantic import BaseModel, root_validator
from .singleton import Singleton_BaseModel
from .backend import BackendSchema
import typing
import os


class StorageSchema(Singleton_BaseModel):

    STORAGE: str = "PUREML-STORAGE"
    backend: BackendSchema = BackendSchema().get_instance()

    class Config:
        arbitrary_types_allowed = True
