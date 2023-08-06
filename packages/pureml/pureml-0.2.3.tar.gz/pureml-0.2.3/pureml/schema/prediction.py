from pydantic import BaseModel
from .backend import BackendSchema

from .paths import PathSchema
import os


class PredictionSchema(BaseModel):
    paths: PathSchema = PathSchema().get_instance()
    backend: BackendSchema = BackendSchema().get_instance()

    PATH_PREDICT_REQUIREMENTS: str = os.path.join(
        paths.PATH_PREDICT_DIR, "requirements.txt"
    )
    PATH_PREDICT: str = os.path.join(paths.PATH_PREDICT_DIR, "predict.py")

    PATH_PREDICT_USER: str = os.path.join(os.getcwd(), "predict.py")
    PATH_PREDICT_REQUIREMENTS_USER: str = os.path.join(os.getcwd(), "requirements.txt")

    class Config:
        arbitrary_types_allowed = True
