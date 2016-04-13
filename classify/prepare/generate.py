#!/usr/bin/env python3

import random


def generate_vector():
    return [random.randint(0, 35) for _ in range(8)]


def check(v):
    if not (v[0]**2 + v[1]**2 + v[2]**2 <= 20**2 and
            10**2 < (v[3]**2 + v[4]**2 + v[6]**2) <= 30**2 and
            25 < v[0] + v[2] + v[4] + v[7]):
        return 0

    return 1 + int(10*v[5]/36)


def generate(fn, n):
    with open(fn, 'w') as f:
        for _ in range(n):
            vec = generate_vector()
            print("{} {}".format(check(vec), ' '.join(
                "{}:{}".format(i + 1, x) for (i, x) in enumerate(vec))),
                file=f)

if __name__ == '__main__':
    generate('train.txt', 50000)
