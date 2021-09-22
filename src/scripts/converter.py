'''
Converts sgr/graph file to gfa file.
'''

#!/usr/bin/python3
import argparse

def main(filename):
    convert_to_sgr(filename)

def convert_file(filename):
    '''
    Converts given sgr/graph file to gfa file.
    '''
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == '#':
                print(f'H {line.rstrip()}')
            elif len(line.split(' ')) > 1:
                print(edge_to_gfa(line))


def covert_to_sgr(filename):
    with open(filename, 'r') as f:
        for line in f:
            if line[0] == 'H':
                print(f'# {line.rstrip()}')
            else:
                pass
                # TODO: prosess sg file's edges such that nodes are represented as integers
                # format of sgr file https://github.com/Kingsford-Group/catfish/blob/master/examples/input.sgr

def edge_to_gfa(line):
    '''
    Converts given sgr/graph path to gfa path.
    '''
    split_line = (line.rstrip()).split()
    return f'L\t{split_line[0]}\t+\t{split_line[1]}\t+\t{int(float(split_line[2]))}M'
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="path to file")
    args = parser.parse_args()
    main(args.file)
