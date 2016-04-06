#!/usr/bin/env python3

import io
import itertools
import os
import os.path
import random
import sys
import tarfile
from PIL import Image, ImageDraw

from taskutils import BaseTask, md5


FLAG_PREFIX = 'RUCTF'
FLAG_ABC = '123456789_ABCDEFGHIJKLMNPQRSTUVWXYZ' # '0' and 'O' missing


def _generate_picture():
    flag = FLAG_PREFIX + ''.join(random.choice(FLAG_ABC) for _ in range(16))

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


class Task(BaseTask.create(
    NAME='splitting', CATEGORY='ppc', SCORE=100,
    HTML_EN="Find the flag", HTML_RU="Найдите флаг", DB_FILE='flags.db')):
    PARTS = 50

    @BaseTask.cmd("create")
    def cmd_create(self, dump_dir, team_id):
        (fn, quid) = Task.prepare_task(dump_dir, 'data.tar',
                                       create_task, Task.PARTS)
        Task.print_task_info(quid, fn)

    @BaseTask.cmd("user")
    def cmd_user(self, dump_dir, quid):
        code = Task.check_task(dump_dir, quid)
        return (0 if code else 1)


def main(args):
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=True)
    return Task().run(*args)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
