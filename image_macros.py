from typing import Dict, List

from PIL import Image
from io import BytesIO
import requests
import random
import json
from bs4 import BeautifulSoup

def pick_random_mugshot(character_list: Dict[str, List[str]]) -> Image.Image:
    character = random.choice(list(character_list.keys()))
    mugshot_url = random.choice(character_list[character])

    image_download = requests.get(mugshot_url, timeout=5)
    if not image_download.ok:
        raise RuntimeError("timed out waiting for mugshot download")
    
    mugshot = Image.open(BytesIO(image_download.content))
    if mugshot.size == (300, 171): # "image not found"
        raise RuntimeError("image not found")
    
    return mugshot


