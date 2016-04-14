#!/usr/bin/env python3

import itertools
import os.path
import random
import sys

from taskutils import BaseTask


FLAG_PREFIX = 'RUCTF'
FLAG_ABC = '1234567890_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CIPHER_ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CIPHER_DICT = {c: i for (i, c) in enumerate(CIPHER_ABC)}


def create_task():
    with open('text.txt') as f:
        text = f.read().split()

    flag = FLAG_PREFIX + ''.join(random.choice(FLAG_ABC) for _ in range(16))
    text.insert(random.randrange(len(text)), flag)
    text = ' '.join(text)

    key = [CIPHER_DICT[random.choice(CIPHER_ABC)]
           for _ in range(len(FLAG_PREFIX) + 5)]

    text = ''.join((
        CIPHER_ABC[(CIPHER_DICT[t] + k)%len(CIPHER_ABC)]
        if t in CIPHER_DICT else t)
        for (t, k) in zip(text, itertools.cycle(key)))

    return (flag, text)


class Task(BaseTask.create(
    NAME='vigenere', CATEGORY='crypto', SCORE=100, DB_FILE='flags.db',
    HTML_EN="Decrypt the text: <pre>{}</pre>",
    HTML_RU="Расшифруйте текст: <pre>{}</pre>")):

    @BaseTask.cmd("create")
    def cmd_create(self, dump_dir, team_id):
        (flag, text) = create_task()
        quid = Task.store_flag(os.path.join(dump_dir, Task.DB_FILE), flag)
        print("ID:{}".format(quid))
        print("html[en]:{}".format(Task.HTML_EN.format(text)))
        print("html[ru]:{}".format(Task.HTML_RU.format(text)))

    @BaseTask.cmd("user")
    def cmd_user(self, dump_dir, quid):
        code = Task.check_task(dump_dir, quid)
        return (0 if code else 1)


def main(args):
    sys.stdout = open(1, 'w', encoding='utf-8', closefd=True)
    return Task().run(*args)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
