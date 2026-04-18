import json 
import os 

CONFIG_FILE = "config.json"

def get_mongo_uri(): 
    if not os.path.exists(CONFIG_FILE): 
        return None
    
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    
    return data.get("mongo_uri")

def save_mongo_uri(uri): 

    with open(CONFIG_FILE, "w") as f: 
        json.dump({"mongo_uri":uri}, f)
    