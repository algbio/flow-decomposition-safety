'''
Comparing safety or catfish result to truth file
'''
#!/usr/bin/python3
import argparse
import numpy as np
import pandas as pd
from src.scripts import io_helper


def main(truth, output, catfish=None, safety=None):
    '''
    Main method for comparing graphs files. Outputs a file where
    each comparison result for compared graphs is reported.
    Gets paths to cafish or safety, truth and output files as a parameter.
    '''

    graphs = io_helper.read_file(
        catfish, 'catfish') if catfish else io_helper.read_file(safety, 'safety')

    truth_graphs = io_helper.read_file(truth, 'truth')

    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(graphs)
    else:
        print('graphs don\'t match. comparison can\'t be done')
        return

    io_helper.write_file(
        'graph,precision,max_cov_rel,number_of_paths,number_of_paths_truth,paths_length_sum\n', f'{output}')
    for i in range(0, n):
        row = {'graph': i,
               'precision': [precision(graphs[i], truth_graphs[i])],
               'max_cov_rel': [max_cov_rel(graphs[i], truth_graphs[i])],
               'number_of_paths': [len(graphs[i])],
               'number_of_paths_truth': [len(truth_graphs[i])],
               'sum_of_path_length': [np.sum([len(path) for path in graphs[i]])]
               }
        io_helper.write_file(pd.DataFrame(row).to_csv(header=False), f'{output}')



def precision(graph, truth_graph):
    '''
    recision(graph, truth_graph) -> float
    Returns how many paths in graph were included in truth graph paths
    Path is included if it is contained as a whole in (some) truth path.
    '''
    included = 0
    number_of_paths = len(graph)
    for path in graph:
        for true_path in truth_graph:
            if correct(path, true_path):
                included += 1
                break
    return included/number_of_paths


def correct(path, truth_path):
    '''
    correct(path, truth_path) -> Boolean
    Return True if path is included in truth path as a whole, if not returns False.
    '''
    return str(path)[1:-1] in str(truth_path)

def max_cov_rel(graph, truth_graph):
    '''
    max_cov_rel(graph, truth_graph) -> float
    For each path in truth graph longest overlap with graph path is calculated
    Overlap value for each truth path per graph are added together in variable total
    Total is then divided by number of paths in truth graph and returned
    as a average overlap.
    '''
    total = 0
    number_of_paths = len(truth_graph)

    for truth_path in truth_graph:
        best_overlap_for_truth_path = 0
        for path in graph:
            paths_longest_overlap = longest_overlap(path, truth_path)
            if paths_longest_overlap > best_overlap_for_truth_path:
                best_overlap_for_truth_path = paths_longest_overlap
        total += best_overlap_for_truth_path/len(truth_path)

    return total/number_of_paths


def longest_overlap(path, truth_path):
    '''
    longest_overlap(path, truth_path) -> integer
    Computes longest overlap of two paths using two pointer method.
    '''
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish_input", default=None)
    parser.add_argument("-s", "--safety_input", default=None)
    parser.add_argument("-t", "--truth_input", default=None)
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    main(args.truth_input, args.output_file,
         args.catfish_input, args.safety_input)
