from typing import Dict, List, Tuple

from PIL import Image
from io import BytesIO
import requests
import random
import json
from bs4 import BeautifulSoup

Coords = List[int]

def pick_random_mugshot(mugshot_urls: List[str]) -> Image.Image:

    mugshot_url = random.choice(mugshot_urls)

    try:
        mugshot = Image.open(f"img/cache/{mugshot_url.split('/')[-3]}.png")
    except:
        max_retries = 3
        image_download = None
        for i in range(max_retries):
            try:
                image_download = requests.get(mugshot_url, timeout=5)
            except requests.exceptions.ReadTimeout:
                mugshot_url = random.choice(mugshot_urls)
                image_download = None
                continue
            break
        
        if image_download is None: 
            return
        
        if not image_download.ok:
            return None
        
        mugshot = Image.open(BytesIO(image_download.content))
        if mugshot.size == (300, 171): # "image not found"
            raise RuntimeError("image not found")
        
        with open(f"img/cache/{mugshot_url.split('/')[-3]}.png", "wb") as img_cached:
            mugshot.save(img_cached, "PNG")

    return mugshot

def random_template() -> Tuple[Image.Image, int, List[Coords]]:

    images = dict()

    with open("img/img_info.json") as info:
        images = json.load(info)
    
    template_name = random.choice(list(images.keys()))

    template_image = Image.open(f"img/{template_name}")
    template_mugshot_coords = images[template_name]["coords"]
    template_mugshot_size = images[template_name]["size"]
    min_mugshots = images[template_name].get("min_mugshots", 1)

    return template_image, template_mugshot_size, template_mugshot_coords, min_mugshots

def generate_image_macro(character_info: Dict[str, List[str]]):
    template_image, template_mugshot_size, template_mugshot_coords, min_mugshots = random_template()

    random.shuffle(template_mugshot_coords)

    characters = set()
    while len(characters) < random.randint(min_mugshots, len(template_mugshot_coords)):
        characters.add(random.choice(list(character_info.keys())))
    
    for i,character in enumerate(iter(characters)):
        mugshot_raw = pick_random_mugshot(character_info[character])
        if mugshot_raw is None:
            continue
        mugshot = mugshot_raw.resize((template_mugshot_size, template_mugshot_size))

        template_image.paste(
            mugshot,
            tuple(template_mugshot_coords[i])
        )

    return template_image

