import abc
import hashlib
import random


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
        def cmd_id(self):
            print("{}:{}".format(cls.CATEGORY, cls.SCORE))

        @BaseTask.cmd("series")
        def cmd_series(self):
            print(cls.CATEGORY)

        @BaseTask.cmd("name")
        def cmd_name(self):
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
