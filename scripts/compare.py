#!/usr/bin/python3
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-co", "--catfish_output", help="path to file")
    parser.add_argument("-so", "--safety_output")
    parser.add_argument("-gt", "--ground_truth")
    args = parser.parse_args()
    compare_files(args.catfish_output, args.safety_output, args.ground_truth)


def compare_files(catfish, safety, truth):
    with open(catfish, 'r') as e, open(safety, 'r') as f, open(truth, 'r') as g:
        read_1 = e.readline()
        read_2 = f.readline()
        read_3 = g.readline()
        i = 0
        while i < 5:
            write_file(f'comparison of {read_2}')
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

            catfish_ver = []
            for p in catfish_graph:
                p_temp = []
                s = (p.rstrip()).split(',')
                for d in s[2].split(' '):
                    if d != 'vertices' and d != '=' and len(d) > 0:
                        p_temp.append(d)
                catfish_ver.append(p_temp)
            print(catfish_ver)

            safety_ver = []
            for p in safety_graph:
                safety_ver.append((p.rstrip().split(' ')))
            print(safety_ver)
            truth_ver = []
            for v in truth_graph:
                s = (v.rstrip()).split(' ')
                truth_ver.append([x for x in s[1:len(s)]])
            print(truth_ver)

            # comparison of all paths here

            print("*******")
            i += 1


def write_file(str):
    f = open('data/comp.txt', 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
