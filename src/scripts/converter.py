'''
Converts sgr/graph file to gfa file.
'''

#!/usr/bin/python3
import argparse
from src.scripts import io_helper
from timeit import default_timer as timer


def main(filename):
    convert_file(filename)


def convert_file(filename):
    '''
    Converts given sgr/graph file to gfa file.
    '''
    output = f'{filename}.gfa'
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                io_helper.write_file(f'H {line}', output)
            elif len(line.split(' ')) > 1:
               io_helper.write_file(to_gfa(line), output)


def to_gfa(line):
    '''
    Concerts given sgr/graph path to gfa path.
    '''
    split_line = (line.rstrip()).split()
    return f'L\t{split_line[0]}\t+\t{split_line[1]}\t+\t{int(float(split_line[2]))}M\n'
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="path to file")
    parser.add_argument("-t", "--timer", help="Boolean: timer is used, default False", default=False)
    args = parser.parse_args()
    if args.timer:
        main_start = timer()
        main(args.file)
        main_end = timer()
        print('executing the whole code')
        print(f'{main_end-main_start}s')
    else:
        main(args.file)
