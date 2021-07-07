#!/usr/bin/python3
import argparse
import os
import io_helper


def main():
    # if os.path.isfile('data/comp.txt'):
    #    os.remove('data/comp.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    summary = {}
    for root, dirs, files in os.walk(args.input_folder):
        for f in files:
            filename = f'{root}{f}'
            print(filename)
            with open(filename, 'r') as f:
                number_of_paths = 0
                for line in f:
                    parts = line.rstrip().split(' ')
                    if parts[0] == 'number_of_paths_in_truth_graph':
                        number_of_paths = int(parts[1])
                        if number_of_paths in summary:
                            summary[number_of_paths]['n'] += 1
                        else:
                            summary[number_of_paths] = {
                                'n': 1, 'pre': 0, 'max': 0}
                    elif parts[0] == 'precision':
                        summary[number_of_paths]['pre'] += float(parts[1])
                    elif parts[0] == "max_cov_rel":
                        summary[number_of_paths]['max'] += float(parts[1])

    print(summary)
    print('averages')
    for i in list(sorted(summary)):
        print(f'k: {i}')
        print(f'n: {summary[i]["n"]}')
        print(f'precision: {summary[i]["pre"] / summary[i]["n"]}')
        print(f'max coverage: {summary[i]["max"] / summary[i]["n"]}')


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
