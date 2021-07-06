#!/usr/bin/python3
import argparse
from operator import le
import os
import io_helper


def main():
    if os.path.isfile('data/comp.txt'):
        os.remove('data/comp.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--first_input")
    parser.add_argument("-t", "--truth_input")
    parser.add_argument("-o", "--output_file",)
    args = parser.parse_args()
    graphs_1 = io_helper.read_file(args.first_input, 'safety')
    graphs_2 = io_helper.read_file(args.truth_input)
    precision(graphs_1, graphs_2, args.output_file)
    max_cov_rel(graphs_1, graphs_2, args.output_file)


def precision(graphs, truth_graphs, output):
    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(graphs)
    included = 0
    all_paths = 0
    for i in range(0, n):
        all_paths += len(graphs[i])
        for path in graphs[i]:
            for true_path in truth_graphs[i]:
                if correct(path, true_path):
                    included += 1
                    break

    print(f'{included}/{all_paths} = {included/all_paths}')
    write_file('precision', output)
    write_file(f'{included/all_paths}', output)


def correct(path, truth_path):
    return str(path)[1:-1] in str(truth_path)

# safety results are too good?
def max_cov_rel(graphs, truth_graphs, output):
    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(graphs)
    total = 0
    number_of_paths = 0

    for i in range(0, n):
        for truth_path in truth_graphs[i]:
            max = 0
            for path in graphs[i]:
                val = longest_overlap(path, truth_path)
                if val > max:
                    max = val
            total += max/len(truth_path)
            print(f'{max}\{len(truth_path)}={total}')
            if max > len(truth_path):
                print('sos')
            number_of_paths += 1

    print(total/number_of_paths)
    write_file('max_cov_rel', output)
    write_file(f'{total/number_of_paths}', output)


def longest_overlap(path, truth_path):
    n = len(truth_path)
    m = len(path)
    max = 0
    sub_lengths = [0 for x in range(m)]
    for i in range(0, n):
        for j in range(m-1, -1, -1):
            if truth_path[i] == path[j]:
                if j > 0:
                    sub_lengths[j] = sub_lengths[j-1]
                    sub_lengths[j] += 1
                else:
                    sub_lengths[j] = 1
                if sub_lengths[j] > max:
                    max = sub_lengths[j]
            else:
                sub_lengths[j] = 0
    return max


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
