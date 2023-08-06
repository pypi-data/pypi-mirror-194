from pydantic import BaseModel
from .paths import PathSchema
from .backend import BackendSchema
import os


class LogSchema(BaseModel):
    paths: PathSchema = PathSchema().get_instance()
    backend: BackendSchema = BackendSchema().get_instance()
