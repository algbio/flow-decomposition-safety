'''
Main class for using safety algorithm
'''
#!/usr/bin/python3
import argparse
from src.scripts import io_helper
from timeit import default_timer as timer


def main(input_file, output_file, timer = False):
    graphs = io_helper.read_gfa_file(input_file)
    i = 0
    algotime = 0
    decompositiontime = 0
    safetytime = 0
    for g in graphs:
        io_helper.write_file(f'# graph {i}\n', output_file)
        if timer:
            start = timer()
        g.maximal_safety()
        if timer:
            end = timer()
            algotime += (end-start)
            decompositiontime += g.get_decomposition_time()
            safetytime += g.get_safety_time()
        io_helper.write_file(g.safe_paths_to_string(), output_file)
        i += 1
    if timer:
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
            str += f'{p[1]}\n'
        i += 1
    return str


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--graph_file", help="path to input file")
    parser.add_argument("-o", "--output_file", help="path to output file")
    parser.add_argument("-t", "--timer", help="measure how long the execution takes, default: False", default=False)
    args = parser.parse_args()

    file = args.graph_file
    if args.timer:
        main_start = timer()
        main(args.graph_file, args.output_file)
        main_end = timer()
        print('executing the whole code')
        print(f'{main_end-main_start}s')
    else:
        main(args.graph_file, args.output_file)
