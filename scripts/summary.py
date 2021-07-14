#!/usr/bin/python3
import argparse
import os
import io_helper
# change ths to use dataframes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    # summary is collection {k: {'n':(int), 'max':(float), 'pre':(float), 'n2':(int), 'avg_len':(int)}}
    # where k is integer number representing number of paths in truth graph
    # 'n' notes how many times graph with k paths is occured
    # 'max' is a sum of maximum coverage values of all size k graphs
    # 'pre' is a sum of all precision values of size k graphs
    # 'n2' is number of paths in safety/catfish file
    # 'len_sum' is sum of lengths of paths
    summary = {}

    for root, dirs, files in os.walk(args.input_folder):
        for file in files:
            filename = f'{root}/{file}'
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
                                'n': 1, 'pre': 0, 'max': 0, 'n2': 0, 'len_sum': 0, 'sum_of_paths': 0, 'sum_of_lengths': 0}
                    elif parts[0] == 'precision':
                        summary[number_of_paths]['pre'] += float(parts[1])
                    elif parts[0] == "max_cov_rel":
                        summary[number_of_paths]['max'] += float(parts[1])
                    elif parts[0] == 'n_paths':
                        summary[number_of_paths]['n2'] += int(parts[1])
                    elif parts[0] == 'avg_path_length':
                        summary[number_of_paths]['len_sum'] += float(parts[1])
                    elif parts[0] == 'n_paths':
                        summary[number_of_paths]['sum_of_paths'] += int(parts[1])
                    elif parts[0] == 'sum_of_path_lengths':
                        summary[number_of_paths]['sum_of_lengths'] += float(parts[1])

    print(summary)
    print('averages')
    for i in list(sorted(summary)):
        print(f'k: {i}')
        print(f'n: {summary[i]["n"]}')
        print(f'precision: {summary[i]["pre"] / summary[i]["n"]}')
        print(f'max coverage: {summary[i]["max"] / summary[i]["n"]}')
        write_file(f'k: {i}', args.output_file)
        write_file(f'n: {summary[i]["n"]}', args.output_file)
        write_file(
            f'precision: {summary[i]["pre"] / summary[i]["n"]}', args.output_file)
        write_file(
            f'max coverage: {summary[i]["max"] / summary[i]["n"]}', args.output_file)
        write_file(f'number of paths in compared file: {summary[i]["sum_of_paths"]}', args.output_file)
        write_file(
            f'average length of the path in compared file: {summary[i]["sum_of_lengths"]/summary[i]["sum_of_paths"]}', args.output_file)


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
