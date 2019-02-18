import pkg_resources
import json


def get_from_config(key):
    file_path = pkg_resources.resource_filename("utils", "config/settings.json")

    with open(file_path, "r") as in_file:
        settings = json.load(in_file)

    return settings.get(key)
