import json
import base64
from io import BytesIO
from flask import Flask, request, render_template

import characters as char
import meme_templates as templates
import image_macros as images

def load_config() -> dict:
    with open("conf/config.json") as config:
        return json.load(config)

def create_app():
    config = load_config()

    characters = char.generate_character_list(
        config.get("use_stored_characters", False)
    )

    app = Flask(__name__)

    @app.route("/")
    def home_page():
        return render_template("home.html")


    @app.route("/characters")
    def character_list():
        character_names = list(sorted(list(characters.keys())))
        return render_template("generated.html", gen=character_names, category="characters", title="Characters")


    @app.route("/generate/<category>")
    def generate_template(category: str):

        category = category.strip().lower()

        if category == "image":
            image = images.generate_image_macro(characters)
            with BytesIO() as output:
                image.save(output, format="PNG")
                image_bytes = output.getvalue()
            
            encoded = base64.b64encode(image_bytes).decode()

            generated = [encoded]
        else:
            num_quotes = int(request.args.get('num', 1))
            generated = [templates.random_template(category, characters) for _ in range(num_quotes)]

        return render_template("generated.html", gen=generated, category=category)

    return app