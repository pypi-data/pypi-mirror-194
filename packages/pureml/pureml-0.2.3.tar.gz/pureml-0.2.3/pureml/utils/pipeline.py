from .config import load_config, save_config
from .hash import generate_hash_for_dict, generate_hash_for_function
from .source_code import get_source_code
import os
import shutil
from .log_utils import update_step_dict


def add_load_data_to_config(name, func=None, hash=""):

    config = load_config()
    code = ""
    if func is not None:
        try:
            code = get_source_code(func)
            hash = generate_hash_for_function(func)
        except Exception as e:
            print("Unable to get load_data source code")
            print(e)

    config["load_data"] = {
        "name": name,
        "hash": hash,
        "type": "load_data",
        "code": code,
    }

    save_config(config=config)


def add_transformer_to_config(name, func=None, hash="", parent=None):

    config = load_config()
    # print(config)
    position = len(config["transformer"]) + 1

    if parent is None:
        if position == 1:

            if len(config["load_data"]) != 0:
                parent = config["load_data"]["name"]

        else:
            transformer_previous = config["transformer"][position - 1]
            parent = transformer_previous["name"]

    code = ""
    if func is not None:
        try:
            code = get_source_code(func)
            hash = generate_hash_for_function(func)
        except Exception as e:
            print("Unable to get transformer source code")
            print(e)

    config["transformer"][position] = {
        "name": name,
        "hash": hash,
        "type": "transformer",
        "parent": parent,
        "code": code,
    }
    # print('saveing configuration for ', name)
    save_config(config=config)


def add_dataset_to_config(name, branch, func=None, hash="", version="", parent=None):

    config = load_config()

    if parent is None:

        if len(config["transformer"]) != 0:
            config_transformer = config["transformer"]
            transformer_last = list(config_transformer.values())[-1]
            parent = transformer_last["name"]

    code = ""
    if func is not None:
        try:
            code = get_source_code(func)
            hash = generate_hash_for_function(func)
        except Exception as e:
            print("Unable to get dataset source code")
            print(e)

    config["dataset"] = {
        "name": name,
        "branch": branch,
        "hash": hash,
        "type": "dataset",
        "version": version,
        "parent": parent,
        "code": code,
    }

    save_config(config=config)


def add_model_to_config(name, branch, func=None, hash="", version=""):
    # name = ''
    # hash = ''
    # version = ''

    config = load_config()

    code = ""
    if func is not None:
        try:
            code = get_source_code(func)
            hash = generate_hash_for_function(func)
        except Exception as e:
            print("Unable to get model source code")
            print(e)

    # Empty hash is passed to create the empty model with just model name the first time
    # Complete hash is passed to create the model with all the details in the second time
    if hash == "":
        position = len(config["model"]) + 1

        config["model"][position] = {
            "name": name,
            "branch": branch,
            "hash": hash,
            "version": version,
            "code": code,
        }
    else:
        position = len(config["model"])
        model_name_position = config["model"][position]["name"]
        if model_name_position == name:
            config["model"][position]["branch"] = branch
            config["model"][position]["hash"] = hash
            config["model"][position]["version"] = version
            config["model"][position]["code"] = code

    save_config(config=config)


def add_metrics_to_config(
    values, model_name=None, model_branch=None, model_version=None, func=None
):
    config = load_config()

    if model_name is None:
        model_name, model_branch, model_version, model_hash = get_model_latest(
            config=config
        )

    if len(config["metrics"]) != 0:
        metric_values = config["metrics"]["values"]
        # metric_values = update_step_dict(metric_values, values)
        metric_values.update(values)
        # print('default',metric_values)
    else:
        metric_values = values

        # print('not default',metric_values)

    hash = generate_hash_for_dict(values=metric_values)

    config["metrics"].update(
        {
            "values": metric_values,
            "hash": hash,
            "model_name": model_name,
            "model_branch": model_branch,
            "model_version": model_version,
        }
    )

    save_config(config=config)


def load_metrics_from_config():

    config = load_config()
    try:
        metrics = config["metrics"]["values"]
    except Exception as e:
        # print(e)
        print("No metrics are found in config")
        metrics = {}

    return metrics


def add_params_to_config(
    values, model_name=None, model_branch=None, model_version=None, func=None
):
    config = load_config()

    if model_name is None:
        model_name, model_branch, model_version, model_hash = get_model_latest(
            config=config
        )

    if len(config["params"]) != 0:
        param_values = config["params"]["values"]
        # param_values = update_step_dict(param_values, values)
        param_values.update(values)
    else:
        param_values = values

    hash = generate_hash_for_dict(values=param_values)

    config["params"].update(
        {
            "values": param_values,
            "hash": hash,
            "model_name": model_name,
            "model_branch": model_branch,
            "model_version": model_version,
        }
    )

    save_config(config=config)


def load_params_from_config():

    config = load_config()
    try:
        metrics = config["params"]["values"]
    except Exception as e:
        # print(e)
        print("No params are found in config")
        metrics = {}

    return metrics


def add_figures_to_config(
    values, model_name=None, model_branch=None, model_version=None, func=None
):
    config = load_config()

    if model_name is None:
        model_name, model_branch, model_version, model_hash = get_model_latest(
            config=config
        )

    if len(config["figure"]) != 0:
        figure_values = config["figure"]["values"]
    else:
        figure_values = values

    hash = generate_hash_for_dict(values=figure_values)

    config["figure"].update(
        {
            "values": figure_values,
            "hash": hash,
            "model_name": model_name,
            "model_branch": model_branch,
            "model_version": model_version,
        }
    )

    save_config(config=config)


def load_figures_from_config():

    config = load_config()
    try:
        figures = config["figure"]["values"]
    except Exception as e:
        # print(e)
        print("No figures are found in config")
        figures = {}

    return figures


def add_artifacts_to_config(name, values, func):
    hash = ""
    version = ""
    config = load_config()

    model_name, model_branch, model_version, model_hash = get_model_latest(
        config=config
    )

    position = len(config["artifacts"]) + 1
    config["artifacts"][position] = {
        "name": name,
        "hash": hash,
        "version": version,
        "model_name": model_name,
        "model_version": model_version,
    }


def get_model_latest(config, version="latest"):
    config_model = config["model"]
    model_name = None
    model_version = None
    model_hash = None

    model_positions = list(config_model.keys())

    if len(model_positions) != 0:
        # print(model_positions)
        position = model_positions[-1]
        model_name = config_model[position]["name"]
        model_branch = config_model[position]["branch"]
        model_version = config_model[position]["version"]
        model_hash = config_model[position]["hash"]

    return model_name, model_branch, model_version, model_hash
