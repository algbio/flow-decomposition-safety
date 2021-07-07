#!/usr/bin/python3
import argparse
import os
import io_helper


def main():
    # if os.path.isfile('data/comp.txt'):
    #    os.remove('data/comp.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--first_input")
    parser.add_argument("-t", "--truth_input")
    parser.add_argument("-o", "--output_file",)
    args = parser.parse_args()
    graphs = io_helper.read_file(args.first_input)
    truth_graphs = io_helper.read_file(args.truth_input)
    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(graphs)
    else:
        print('graphs don\'t match. comparison can\'t be done')
        return
    for i in range(0, n):
        precision_value = precision(graphs[i], truth_graphs[i])
        max_cov_rel_value = max_cov_rel(graphs[i], truth_graphs[i])
        write_file(f'graph {i}', args.output_file)
        write_file(
            f'number_of_paths_in_truth_graph {len(truth_graphs[i])}', args.output_file)
        write_file(f'precision {precision_value}', args.output_file)
        write_file(f'max_cov_rel {max_cov_rel_value}', args.output_file)


def precision(graph, truth_graph):
    included = 0
    number_of_paths = len(graph)
    for path in graph:
        for true_path in truth_graph:
            if correct(path, true_path):
                included += 1
                break

    print(f'{included}/{number_of_paths} = {included/number_of_paths}')
    return included/number_of_paths


def correct(path, truth_path):
    return str(path)[1:-1] in str(truth_path)


def max_cov_rel(graph, truth_graph):
    total = 0
    number_of_paths = len(truth_graph)

    for truth_path in truth_graph:
        best_overlap_for_truth_path = 0
        for path in graph:
            paths_longest_overlap = longest_overlap(path, truth_path)
            if paths_longest_overlap > best_overlap_for_truth_path:
                best_overlap_for_truth_path = paths_longest_overlap
        total += best_overlap_for_truth_path/len(truth_path)

    print(total/number_of_paths)
    return total/number_of_paths


def longest_overlap(path, truth_path):
    n = len(truth_path)
    m = len(path)
    max = 0
    sub_lengths = [0 for x in range(m)]
    for i in range(0, n):
        for j in range(m-1, -1, -1):
            if truth_path[i] == path[j]:
                if j > 0:
                    sub_lengths[j] = sub_lengths[j-1]
                    sub_lengths[j] += 1
                else:
                    sub_lengths[j] = 1
                if sub_lengths[j] > max:
                    max = sub_lengths[j]
            else:
                sub_lengths[j] = 0
    return max


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    main()
