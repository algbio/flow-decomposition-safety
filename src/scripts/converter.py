'''
Converts sgr/graph file to gfa file.
'''

#!/usr/bin/python3
import argparse
from src.scripts import io_helper


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
               io_helper.write_file(edge_to_gfa(line), output)
            # I do not think this is a good idea, write_file opens the file every time it is called, but it could be opened
            # once here and call write instead.


def edge_to_gfa(line):
    '''
    Converts given sgr/graph path to gfa path.
    '''
    split_line = (line.rstrip()).split()
    return f'L\t{split_line[0]}\t+\t{split_line[1]}\t+\t{int(float(split_line[2]))}M\n'
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="path to file")
    args = parser.parse_args()
    main(args.file)
