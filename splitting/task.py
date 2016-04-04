#!/usr/bin/env python3

import io
import itertools
import os.path
import random
import sys
import tarfile
from PIL import Image, ImageDraw


PREFIX = 'RUCTF'
FLAG_STR = '123456789_ABCDEFGHIJKLMNPQRSTUVWXYZ' # '0' and 'O' missing


def _generate_picture():
    flag = PREFIX + ''.join(random.choice(FLAG_STR) for _ in range(8))

    (w, h) = (256, 64)
    image = Image.new("RGB", (w, h), "white")
    draw = ImageDraw.Draw(image)

    for point in itertools.product(range(w), range(h)):
        draw.point(point, tuple(random.randrange(256) for _ in range(3)))

    (tw, th) = draw.textsize(flag)
    (tx, ty) = ((w - tw)//2, (h - th)//2)

    draw.rectangle((tx - 2, ty - 2, tx + tw + 2, ty + th + 2), "white")
    draw.text((tx, ty), flag, "black")

    stream = io.BytesIO()
    image.save(stream, "JPEG")

    return (flag, stream.getvalue())


def _split_data(data, parts):
    assert parts > 1

    length = len(data)
    cuts = []

    while not cuts or len(set(cuts)) < len(cuts):
        cuts = [random.randrange(1, length) for _ in range(2*(parts - 1))]
        cuts = sorted(cuts)

    result = [data[:cuts[1]], data[cuts[-2]:]]
    result.extend(data[cuts[2*i]:cuts[2*i + 3]] for i in range(parts - 2))

    random.shuffle(result)

    return result


def create_task(filename, parts):
    (flag, data) = _generate_picture()
    chunks = _split_data(data, parts)

    with tarfile.TarFile(filename, 'w') as f:
        for (i, part) in enumerate(chunks):
            info = tarfile.TarInfo()
            info.name = "{}.bin".format(i + 1)
            info.size = len(part)
            f.addfile(info, io.BytesIO(part))

    return flag


def parse_args():
    return None


def main(args):
    params = parse_args()

    print(create_task(args[0], 100))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
