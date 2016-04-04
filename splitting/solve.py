#!/usr/bin/env python3

import argparse
import io
import itertools
import sys
from collections import namedtuple
from os.path import basename, splitext

import strlib


Graph = namedtuple('Graph', ('graph', 'edges'))


def find_start(data):
    for fn in data:
        if b'JFIF' in data[fn][:16]:
            return fn

    return None


def make_graph(data):
    edges = {}

    items = list(data.keys())
    graph = {v: set() for v in items}

    for (first, second) in itertools.product(items, items):
        if first == second:
            continue

        inter = list(strlib.find_intersect(data[first], data[second]))
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
            yield path

        visited = set(path)

        for next_v in (v for v in graph[vertex] if v not in visited):
            queue.append((next_v, path + [next_v]))


def restore_file(data, graph, chain):
    graph = graph.edges

    for common in itertools.product(*(
        graph[chain[i], chain[i + 1]] for i in range(len(chain) - 1))):
        stream = io.BytesIO()
        for (part, offset) in zip(chain, [0] + list(common)):
            stream.write(data[part][offset:])
        yield stream.getvalue()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--start', type=str, metavar='START',
                        help='start vertex')
    parser.add_argument('-o', '--output', type=str, metavar='PREFIX',
                        default='result_', help='prefix of output files')
    parser.add_argument('files', nargs='+', type=str, metavar='FILES',
                        help='input files')

    return parser.parse_args()


def main(args):
    params = parse_args()

    data = {}
    for fn in params.files:
        with open(fn, 'rb') as f:
            data[splitext(basename(fn))[0]] = f.read()

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
