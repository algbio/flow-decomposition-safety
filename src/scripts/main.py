#!/usr/bin/python3
import argparse
import os
from src.scripts import io_helper
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
    algotime = 0
    decompositiontime = 0
    safetytime = 0
    for g in graphs:
        io_helper.write_file(f'# graph {i}', args.output_file)
        start = timer()
        max = g.maximal_safe_paths()
        end = timer()
        algotime += (end-start)
        decompositiontime += g.get_decomposition_time()
        safetytime += g.get_safety_time()
        for m in max:
            io_helper.write_file(path_to_string(m), args.output_file)
        i += 1
    print('time used to algorithm')
    print(algotime)
    print('time used to decomposition algorithm')
    print(decompositiontime)
    print('time used to safety algorithm')
    print(safetytime)


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
    main_start = timer()
    main()
    main_end = timer()
    print('executing the whole code')
    print(f'{main_end-main_start}s')
