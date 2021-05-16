import json
from flask import Flask

import characters as char

def load_config() -> dict:
    with open("conf/config.json") as config:
        return json.load(config)

config = load_config()

characters = char.generate_character_list(
    config.get("use_stored_characters", False)
)

print(characters["Phoenix Wright"])

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, world!</h1>"