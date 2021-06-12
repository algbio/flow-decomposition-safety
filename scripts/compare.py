#!/usr/bin/python3
import argparse
import os


def main():
    if os.path.isfile('data/comp.txt'):
        os.remove('data/comp.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-co", "--catfish_output", help="path to file")
    parser.add_argument("-so", "--safety_output")
    parser.add_argument("-gt", "--ground_truth")
    parser.add_argument("-o", "--output_file",)
    args = parser.parse_args()
    compare_files(args.catfish_output, args.safety_output, args.ground_truth, args.output_file)


def compare_files(catfish, safety, truth, output):
    with open(catfish, 'r') as e, open(safety, 'r') as f, open(truth, 'r') as g:
        read_1 = e.readline()
        read_2 = f.readline()
        read_3 = g.readline()
        i = 0
        all_same = 0
        catfish_deffers_from_truth = 0
        while len(read_2) != 0:
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

            if catfish_ver != truth_ver:
                write_file(f'comparison of {read_2.rstrip()}', output)
                print_all(catfish_ver, safety_ver, truth_ver, output)
                catfish_deffers_from_truth += 1

            if catfish_ver == truth_ver == safety_ver:
                all_same += 1

            i += 1
        print(f'there was {i} graphs')
        write_file(f'there was {i} graphs', output)
        print(f'which {all_same} are same ')
        write_file(f'which {all_same} are same ', output)
        print(f'times catfish differs from truth {catfish_deffers_from_truth}')


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
