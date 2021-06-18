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
                if len(set(path_1) & set(path_2)) > longest_overlap:
                    longest_overlap = len(set(path_1) & set(path_2))
            acc = longest_overlap/len(path_1)
            total += acc
            number_of_paths += 1

    print(len(graphs_1) == len(graphs_2))
    print(total/number_of_paths)


def compare_files(catfish, safety, truth, output):
    with open(catfish, 'r') as e, open(safety, 'r') as f, open(truth, 'r') as g:
        read_1 = e.readline()
        read_2 = f.readline()
        read_3 = g.readline()
        i = 0
        all_same = 0
        catfish_deffers_from_truth = 0
        while len(read_2) > 2:
            catfish_graph = []
            catfish_graph.append(e.readline())
            while(not catfish_graph[-1].startswith('#') and len(catfish_graph[-1]) > 0):
                catfish_graph.append(e.readline())
            catfish_graph.pop()

            safety_graph = []
            safety_graph.append(f.readline())
            while(not safety_graph[-1].startswith('#') and len(safety_graph[-1]) > 0):
                safety_graph.append(f.readline())
            read_2 = safety_graph.pop()

            truth_graph = []
            truth_graph.append(g.readline())
            while(not truth_graph[-1].startswith('#') and len(truth_graph[-1]) > 0):
                truth_graph.append(g.readline())
            truth_graph.pop()

            catfish_ver = set()
            for p in catfish_graph:
                p_temp = []
                s = (p.rstrip()).split(',')
                for d in s[2].split(' '):
                    if d != 'vertices' and d != '=' and len(d) > 0:
                        p_temp.append(d)
                catfish_ver.add(tuple(p_temp))

            safety_ver = set()
            for p in safety_graph:
                safety_ver.add(tuple(p.rstrip().split(' ')))

            truth_ver = set()
            for v in truth_graph:
                s = (v.rstrip()).split(' ')
                truth_ver.add(tuple([x for x in s[1:len(s)]]))

            # comparison of all paths here

            total = 1
            for t in truth_ver:
                longest_overlap = 0
                for s in safety_ver:
                    # print(s)
                    # print(f'intersection {len(set(t) & set(s))}')
                    if len(set(t) & set(s)) > longest_overlap:
                        longest_overlap = len(set(t) & set(s))
                # print(f'longest overlap for {s} was {longest_overlap}')
                acc = longest_overlap/len(t)
                total *= acc
            write_file(f'graph {i}', output)
            write_file(f'total accuracy {total}', output)

            i += 1


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
