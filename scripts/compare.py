#!/usr/bin/python3
import argparse
import os
import io_helper


def main():
    if os.path.isfile('data/comp.txt'):
        os.remove('data/comp.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", "--first_input")
    parser.add_argument("-i2", "--second_input")
    parser.add_argument("-o", "--output_file",)
    args = parser.parse_args()
    compare_files2(args.first_input, args.second_input, args.output_file)


def compare_files2(file_1, file_2, output):
    graphs_1 = io_helper.read_file(file_1)
    graphs_2 = io_helper.read_file(file_2)
    n = 0
    if len(graphs_1) == len(graphs_2):
        n = len(graphs_1)
    total = 0
    number_of_paths = 0

    for i in range(0, n):
        for path_1 in graphs_1[i]:
            longest_overlap = 0
            for path_2 in graphs_2[i]:
                # fix
                if len(set(path_1) & set(path_2)) > longest_overlap:
                    longest_overlap = len(set(path_1) & set(path_2))
            acc = longest_overlap/len(path_1)
            total += acc
            number_of_paths += 1

    print(total/number_of_paths)


def print_all(a, b, c, output):
    print('catfish:')
    print(a)
    print('safety:')
    print(b)
    print('truth:')
    print(c)
    print('**********')
    write_file('catfish:', output)
    for s in a:
        write_file(f'{s}', output)
    write_file('safety:', output)
    for s in b:
        write_file(s, output)
    write_file('truth:', output)
    for s in c:
        write_file(s, output)
    write_file('**********', output)
    write_file('', output)


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
