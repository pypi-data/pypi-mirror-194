import os
import joblib
from collections import defaultdict, OrderedDict
from pureml.schema import PathSchema


path_schema = PathSchema().get_instance()


def load_config():
    os.makedirs(path_schema.PATH_USER_PROJECT_DIR, exist_ok=True)

    if os.path.exists(path_schema.PATH_CONFIG):
        config = joblib.load(path_schema.PATH_CONFIG)
    else:
        config = defaultdict()

        config["load_data"] = defaultdict()
        config["transformer"] = OrderedDict()
        config["dataset"] = defaultdict()

        config["model"] = OrderedDict()

        config["params"] = defaultdict()
        config["metrics"] = defaultdict()
        config["figure"] = defaultdict()
        config["artifacts"] = defaultdict()

        config["predict"] = defaultdict()

        joblib.dump(config, path_schema.PATH_CONFIG)

    return config


def save_config(config):
    save_dir = os.path.dirname(path_schema.PATH_CONFIG)

    os.makedirs(save_dir, exist_ok=True)
    # print('config')
    # print(config)

    joblib.dump(config, path_schema.PATH_CONFIG)
