#!/usr/bin/env python3

import argparse
import io
import itertools
import sys
import tarfile
from collections import namedtuple


Graph = namedtuple('Graph', ('graph', 'edges'))


def find_start(data):
    for fn in data:
        if b'JFIF' in data[fn][:16]:
            return fn

    return None


def z_func(s):
    z = [0]*len(s)

    (l, r) = (0, 0)
    for i in range(1, len(s)):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])

        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            (l, r) = (i, i + z[i] - 1)

    return z


def find_intersect(first, second):
    z = z_func(second + first)

    for i in range(-min(len(first), len(second)), 0):
        if z[i] == -i:
            yield -i


def make_graph(data):
    edges = {}

    items = list(data.keys())
    graph = {v: set() for v in items}

    for (first, second) in itertools.product(items, items):
        if first == second:
            continue

        inter = list(find_intersect(data[first], data[second]))
        if inter:
            edges[first, second] = inter
            graph[first].add(second)

    return Graph(graph, edges)


def find_all_chains(graph, start):
    graph = graph.graph

    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        if len(path) == len(graph):
            yield path[:]

        visited = set(path)

        for next_v in (v for v in graph[vertex] if v not in visited):
            queue.append((next_v, path + [next_v]))


def restore_file(data, graph, chain):
    graph = graph.edges

    for common in itertools.product(*(
        graph[chain[i], chain[i + 1]] for i in range(len(chain) - 1))):
        stream = io.BytesIO()
        for (part, offset) in zip(chain, itertools.chain([0], common)):
            stream.write(data[part][offset:])
        yield stream.getvalue()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--start', type=str, metavar='START',
                        help='start vertex')
    parser.add_argument('-o', '--output', type=str, metavar='PREFIX',
                        default='result_', help='prefix of output files')
    parser.add_argument('file', type=str, metavar='FILE', help='input file')

    return parser.parse_args()


def main(args):
    params = parse_args()

    data = {}
    with tarfile.open(params.file) as tar:
        for entry in tar:
            with tar.extractfile(entry) as f:
                data[entry.name] = f.read()

    start = params.start or find_start(data)
    if not start:
        return 1

    graph = make_graph(data)
    for path in find_all_chains(graph, start):
        for (i, filedata) in enumerate(restore_file(data, graph, path)):
            with open("{}{}.jpg".format(params.output, i + 1), 'wb') as f:
                f.write(filedata)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
