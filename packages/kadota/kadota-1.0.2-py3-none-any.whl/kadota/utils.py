import os 
import json 

def get_repo_dir():
    dir_this = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(dir_this)

def load_keys():
    # Import json key
    with open(f"{get_repo_dir()}/keys.json", "r") as f:
        return json.load(f)