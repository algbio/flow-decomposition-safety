#!/usr/bin/python3
import argparse
import os


def main():
    print('hello')
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="path to file")
    args = parser.parse_args()
    if os.path.isfile(f'{args.file}.gfa'):
        os.remove(f'{args.file}.gfa')
    read_file(args.file)


def read_file(filename):
    with open(filename, 'r') as f:
        print('asdfdsaf')
        for line in f:
            if line[0] == '#':
                write_file(filename, 'H', line)
            elif len(line.split(' ')) > 1:
                write_file(filename, 'L', line)


def write_file(filename, row, line):
    f = open(f'{filename}.gfa', 'a')
    if row == 'H':
        f.write(f'H {line}')
    elif row == 'L':
        split_line = (line.rstrip()).split(' ')
        line_to_write = f'L\t{split_line[0]}\t+\t{split_line[1]}\t+\t{int(float(split_line[2]))}M\n'
        f.write(line_to_write)


if __name__ == '__main__':
    main()
