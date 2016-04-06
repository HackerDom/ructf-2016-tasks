#!/usr/bin/env python2

from __future__ import print_function

import sys
assert sys.version_info[0] == 2, "Only python2 :'("

import tempfile
import os
from PIL import Image, ImageDraw
from qrtools import QR

try:
    range = xrange
except NameError:
    pass


def qr_data_to_qr(data, tmpfile):
    bitstr = ''.join(bin(ord(c))[2:].rjust(8, '0') for c in data).lstrip('0')
    size = int(len(bitstr)**0.5)

    image = Image.new("1", (2*size, 2*size), 'white')
    draw = ImageDraw.Draw(image)

    ptr = iter(bitstr)
    for y in range(size):
        for x in range(size):
            if next(ptr) == '1':
                draw.rectangle((2*x, 2*y, 2*x + 1, 2*y + 1), 'black')

    image.save(tmpfile, 'PNG')


def solve(filename):
    (_, tmp) = tempfile.mkstemp()

    while True:
        qrpic = QR(margin_size=0, filename=filename)
        if qrpic.decode():
            data = qrpic.data
            if len(data) < 32:
                print(data)
                break

            qr_data_to_qr(data, tmp)
            filename = tmp
        else:
            print('Unable to solve', file=sys.stderr)
            break

    os.unlink(tmp)


if __name__ == '__main__':
    solve(sys.argv[1])
