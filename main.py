#!/usr/bin/env python3

import sys
import re
from PIL import Image
import pytesseract


NAME_COORDS = (210, 590, 520, 670)
CP_COORDS = (220, 70, 460, 150)
HP_COORDS = (400, 700, 450, 740)
STARDUST_COORDS = (410, 1050, 500, 1100)


class Config():
    def __init__(self, coords, is_numeric=False):
        self.coords = coords
        self.is_numeric = is_numeric


CONFIGS = {
    'name': Config(NAME_COORDS),
    'cp': Config(CP_COORDS, True),
    'hp': Config(HP_COORDS, True),
    'stardust': Config(STARDUST_COORDS, True),
}


def extract_number(text):
    try:
        return int(re.search('\d+', text).group())
    except (AttributeError, ValueError) as e:
        raise ValueError("Failed to extract number from {}".format(text)) from e


def process_config(image, config):
    i = image.crop(config.coords)
    text = pytesseract.image_to_string(i)
    if config.is_numeric:
        return extract_number(text)
    return text


def process_image(image):
    data = {}
    for key, config in CONFIGS.items():
        value = process_config(image, config)
        data[key] = value
    return data


def main():
    f = sys.argv[1]
    image = Image.open(f)
    info = process_image(image)
    print(info)


main()

