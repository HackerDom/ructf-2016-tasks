#!/usr/bin/env python3

import itertools
import os.path
import random
import string
import sys
from PIL import Image, ImageDraw


FLAG_PREFIX = 'RUCTF'
FLAG_ABC = '123456789_ABCDEFGHIJKLMNPQRSTUVWXYZ'
FILENAME_ABC = string.ascii_letters + string.digits


def random_tuple(max_value, size):
    return tuple(random.randrange(max_value) for _ in range(size))


def create_background():
    (w, h) = (512, 512)
    image = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(image)

    for point in itertools.product(range(w), range(h)):
        draw.point(point, random_tuple(256, 3))

    return image


def create_picture(background, output_dir, with_flag=False):
    fn = ''.join(random.choice(FILENAME_ABC) for _ in range(16)) + '.JPG'
    image = background.copy()
    draw = ImageDraw.Draw(image)

    for _ in range(512):
        draw.point(random_tuple(512, 2), random_tuple(256, 3))

    if with_flag:
        flag = FLAG_PREFIX + ''.join(
            random.choice(FLAG_ABC) for _ in range(16))

        (tw, th) = draw.textsize(flag)
        draw.rectangle((32, 32, 36 + tw, 36 + th), "white")
        draw.text((34, 34), flag, "black")
    else:
        flag = None

    image.save(os.path.join(output_dir, fn), "JPEG")
    return (fn, flag)


if __name__ == '__main__':
    background = create_background()
    for i in range(256):
        print(':'.join(create_picture(background, sys.argv[1], True)))
