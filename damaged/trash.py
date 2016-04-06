#!/usr/bin/env python3

import os
import os.path
import random
import string
import sys

FILENAME_ABC = string.ascii_letters + string.digits


def random_tuple(max_value, size):
    return tuple(random.randrange(max_value) for _ in range(size))


def create_trash(output_dir):
    files = set()

    for i in range(10000):
        create = random.choice((True, True, True, False))
        if create:
            try:
                fn = ''.join(random.choice(FILENAME_ABC) for _ in range(10))
                fn = os.path.join(output_dir, fn)
                with open(fn, 'wb') as f:
                    f.write(bytes(random_tuple(256, random.randrange(16384))))
            except:
                pass
            else:
                files.add(fn)
        else:
            if files:
                os.unlink(files.pop())


if __name__ == '__main__':
    create_trash(sys.argv[1])
