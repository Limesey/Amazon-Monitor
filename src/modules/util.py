import os
from json import load

def get_json_data():
    with open("config.json", "r") as json_file:
        return load(json_file)

def get_setting(index):
    data = get_json_data()

    return data[index]

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if(name in files):
            return os.path.join(root, name)