from json import load
from json import dump
from datetime import datetime

from modules.util import find_file

cache_path = "src/cache"

def write_file(name, data):
    with open(f"{cache_path}/{name}.json", "w") as outfile:
        dump(data, outfile, indent=4)

def get_cache(name):
    f = find_file(f"{name}.json", cache_path)

    if(not f):
        return None
    else:
        with open(f, "r") as json_file:
            return load(json_file)

def save_cache(name,  data):
    data["last_updated"] = datetime.utcnow().__str__()

    write_file(name, data)