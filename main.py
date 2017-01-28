#!/usr/bin/env python3

import os
import re
import argparse
from PIL import Image, ImageEnhance
import pytesseract


class Config():
    def __init__(self, coords, is_numeric=False, filters=None):
        self.coords = coords
        self.is_numeric = is_numeric
        self.filters = filters if filters is not None else []

    def get_coords(self, image):
        w, h = image.size
        return tuple(self._handle_width(c, w) for c in self.coords)

    def _handle_width(self, value, width):
        if value == 'width':
            return width
        if isinstance(value, str) and value.startswith('width-'):
            return width - int(value[6:])
        return value


def increase_contrast(image, amount):
    #contrast = ImageEnhance.Contrast(image)
    #contrast = ImageEnhance.Sharpness(image)
    #return contrast.enhance(amount)
    image = image.convert('L')
    return image.point(lambda x: 255 if x > 250 else 0, '1')


def extract_number(text):
    try:
        print('attempting to extract number from {}'.format(text))
        return int(re.search('\d+', text).group())
    except (AttributeError, ValueError) as e:
        raise ValueError("Failed to extract number from {}".format(text)) from e


class ImageProcessor():

    DEBUG_FOLDER = 'debug'

    CONFIGS = {
        'name': Config((30, 590, 'width-30', 670)),
        'cp': Config((220, 70, 460, 150), True, filters=[increase_contrast]),
        'hp': Config((400, 700, 450, 740), True),
        'stardust': Config((410, 1050, 500, 1100), True),
    }

    def __init__(self, contrast=1.0, psm=6, debug=False):
        if psm < 0 or psm > 10:
            raise ValueError('psm value must be within range [0, 10]')
        self.contrast = contrast
        self.psm = psm
        self.debug = debug

    def process(self, image):
        data = {}
        for key, config in self.CONFIGS.items():
            value = self._process_config(image, config, key)
            data[key] = value
        return data

    def _process_config(self, image, config, key):
        i = image.crop(config.get_coords(image))
        for f in config.filters:
            i = f(i, self.contrast)
        self._save_if_debug(i, key)
        text = pytesseract.image_to_string(i, config='-psm {}'.format(self.psm))
        if config.is_numeric:
            return extract_number(text)
        return text.strip()

    def _save_if_debug(self, image, name):
        if not self.debug:
            return
        os.makedirs(self.DEBUG_FOLDER, exist_ok=True)
        image.save(os.path.join(self.DEBUG_FOLDER, name + '.png'))


def handle_args():
    parser = argparse.ArgumentParser(description='parse data from a pokemon go screenshot')
    parser.add_argument('screenshot', metavar='PATH', help='path to a pokemon screenshot')
    parser.add_argument('--psm', '-p', type=int, help='send the given number to tesseract with the -psm flag')
    parser.add_argument('--contrast', '-c', type=float, help='control the contrast adjustment')
    parser.add_argument('--debug', '-d', action='store_true', default=False, help='store intermediate images in a local debug folder')
    return parser.parse_args()


def main():
    args = handle_args()
    image = Image.open(args.screenshot)
    processor = ImageProcessor(psm=args.psm, contrast=args.contrast, debug=args.debug)
    info = processor.process(image)
    print(info)


main()

