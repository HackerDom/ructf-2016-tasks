import abc
import hashlib
import os
import os.path
import random
import sys


__all__ = ['BaseTask', 'md5']


class BaseTask(metaclass=abc.ABCMeta):
    _CMD_ATTR = '__command_name'
    NAME = None
    CATEGORY = None
    SCORE = None

    @staticmethod
    def cmd(name):
        def handler(func):
            setattr(func, BaseTask._CMD_ATTR, name)
            return func

        return handler

    def __init__(self):
        cls = type(self)

        @BaseTask.cmd("id")
        def cmd_id(self, *rest):
            print("{}:{}".format(cls.CATEGORY, cls.SCORE))

        @BaseTask.cmd("series")
        def cmd_series(self, *rest):
            print(cls.CATEGORY)

        @BaseTask.cmd("name")
        def cmd_name(self, *rest):
            print(cls.NAME)

        setattr(cls, 'cmd_id', cmd_id)
        setattr(cls, 'cmd_series', cmd_series)
        setattr(cls, 'cmd_name', cmd_name)

    def run(self, command=None, *args):
        for fn in dir(self):
            f = getattr(self, fn)
            if hasattr(f, BaseTask._CMD_ATTR):
                if getattr(f, BaseTask._CMD_ATTR) == command:
                    return f(*args)

        return 1

    @staticmethod
    def create(**kwargs):
        name = "Task_{}".format(kwargs['NAME'])
        return type(name, (BaseTask,), kwargs)

    @classmethod
    def prepare_task(cls, dump_dir, filename, creator=None, *args):
        task_dir = md5(random.random())
        filename = os.path.join(task_dir, filename)
        os.makedirs(os.path.join(dump_dir, task_dir), exist_ok=True)

        if creator:
            flag = creator(os.path.join(dump_dir, filename), *args)
            quid = BaseTask.store_flag(
                os.path.join(dump_dir, cls.DB_FILE), flag)

            return (filename, quid)

        return filename

    @classmethod
    def print_task_info(cls, quid, filename=None):
        print("ID:{}".format(quid))
        print("html[en]:{}".format(cls.HTML_EN))
        print("html[ru]:{}".format(cls.HTML_RU))
        if filename:
            print("file:{}".format(filename))

    @classmethod
    def check_task(cls, dump_dir, quid, answer=None):
        answer = answer or sys.stdin.readline().strip()

        rv = cls.check_flag(os.path.join(dump_dir, cls.DB_FILE), quid, answer)
        print('Correct' if rv else 'Wrong')
        return rv

    @staticmethod
    def store_flag(db_name, flag, quid=None):
        if quid is None:
            quid = md5(random.random())

        with open(db_name, 'a') as f:
            print("{}\t{}".format(quid, flag), file=f)

        return quid

    @staticmethod
    def check_flag(db_name, quid, flag):
        with open(db_name) as f:
            for line in f:
                (id_, flag_) = line.strip().split('\t')
                if quid != id_:
                    continue

                if flag == flag_:
                    return True

        return False


def md5(data):
    h = hashlib.md5()
    h.update(repr(data).encode())
    return h.hexdigest()
