#!/usr/bin/python3
import networkx as nx
import argparse
import os
import io_helper
from timeit import default_timer as timer

def main():
    if os.path.isfile('data/output.txt'):
        os.remove('data/output.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to file")
    parser.add_argument("-o", "--output_file", help="path to file")
    args = parser.parse_args()

    file = args.graph_file
    graphs = io_helper.read_gfa_file(file)
    i = 0
    for g in graphs:
        max = g.maximal_safe_paths()
        io_helper.write_file(f'# graph {i}', args.output_file)
        for m in max:
            io_helper.write_file(path_to_string(m), args.output_file)
        i += 1

def path_to_string(path):
    str = ''
    i = 0
    for p in path:
        str += f'{p[0]} '
        if i == len(path)-1:
            str += f'{p[1]}'
        i += 1
    return str


if __name__ == '__main__':
    main()
