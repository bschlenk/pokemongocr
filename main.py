#!/usr/bin/env python3

import sys
import re
from PIL import Image
import pytesseract


def get_name(image):
    name_image = image.crop((210, 590, 520, 670))
    name_text = pytesseract.image_to_string(name_image)
    return name_text


def get_cp(image):
    # isolate cp in image
    cp_image = image.crop((220, 70, 460, 150))
    # ocr on image
    cp_text = pytesseract.image_to_string(cp_image)
    cp_text = re.search('\d+', cp_text).group()
    try:
        return int(cp_text)
    except ValueError:
        raise ValueError('Failed to process CP value from image')

def get_hp(image):
    hp_image = image.crop((400, 700, 450, 740))
    hp_text = pytesseract.image_to_string(hp_image)
    hp_text = re.search('\d+', hp_text).group()
    return int(hp_text)


def get_powerup_stardust(image):
    i = image.crop((410, 1050, 500, 1100))
    text = pytesseract.image_to_string(i)
    text = re.search('\d+', text).group()
    return int(text)


def get_information(image):
    name = get_name(image)
    cp = get_cp(image)
    hp = get_hp(image)
    powerup_stardust = get_powerup_stardust(image)

    data = locals()
    del data['image']
    return data


def main():
    f = sys.argv[1]
    image = Image.open(f)
    info = get_information(image)
    print(info)


main()

