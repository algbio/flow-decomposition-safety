'''
Comparing safety or catfish result to truth file
'''
#!/usr/bin/python3
import argparse
import numpy as np
from src.scripts import io_helper
import csv
from sys import stdout

def main(truth, catfish=None, comp=None, mode=None):
    '''
    Main method for comparing graphs files. Outputs 
    each comparison result for compared graphs is reported.
    '''
    if mode:
        flow_decs, indices = io_helper.read_index_file(file)
    else:
        graphs = io_helper.read_file(catfish, 'catfish') if catfish else io_helper.read_file(comp)

    truth_graphs = io_helper.read_file(truth, 'truth')
    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(truth_graphs)
    else:
        print('graphs don\'t match. comparison can\'t be done')
        return
    writer = csv.writer(stdout)
    if mode:
        writer.writerow(['graph','precision','max_cov_rel','number_of_paths','k','truth_path_len_sum','path_length_sum','sum_of_paths_through_vertices','number_of_vertices', 'number_flow_dec','flow_dec_path_len_sum'])
    else:
        writer.writerow(['graph','precision','max_cov_rel','number_of_paths','k','truth_path_len_sum','path_length_sum','sum_of_paths_through_vertices','number_of_vertices'])
    for i in range(0, n):
        if mode:
            writer.writerow([i, #number of graph
            0, #preciison
            0, #max_cov_rel
            np.sum([len(p) for p in indices[i]]), #number of paths
            len(truth_graphs[i]), #k
            np.sum([len(path) for path in truth_graphs[i]]),#truth path len sum
            index_path_len_sum(indices[i]), #path len sum
            0, #sum og paths thrug vertices
            0, #number of vertices
            len(flow_decs[i]), #number_flow_dec
            np.sum([len(x) for x in flow_decs[i]]) #flow_dec_path_len_sum
            ])
        writer.writerow([i,#graph
               precision(graphs[i], truth_graphs[i]),#pre
               max_cov_rel(graphs[i], truth_graphs[i]),#max-cov-rel
               len(graphs[i]),#number of paths
               len(truth_graphs[i]),#k
               np.sum([len(path) for path in truth_graphs[i]]),#truth path len sum
               np.sum([len(path) for path in graphs[i]]),#path len sum
               np.sum([x for x in vertex_coverage(graphs[i]).values()]),# sum of paths through vertices
               len(vertex_coverage(graphs[i])) # number of vertices
        ])
    
def index_path_len_sum(paths):
    sum = 0
    for p in paths:
        for i,k in p:
            sum += (k-i)
    return sum

def precision(graph, truth_graph):
    '''
    precision(graph, truth_graph) -> float

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
                    sub_lengths[j] = sub_lengths[j-1] + 1
                else:
                    sub_lengths[j] = 1
                if sub_lengths[j] > max:
                    max = sub_lengths[j]
            else:
                sub_lengths[j] = 0
    return max

def vertex_coverage(graph):
    dic = {}
    for path in graph:
        for v in path:
            if v not in dic:
                dic[v] = 0
            dic[v] += 1
    return dic


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish_input", default=None)
    parser.add_argument("-i", "--input", default=None)
    parser.add_argument("-t", "--truth_input")
    parser.add_argument('-m','--mode', default=None)
    args = parser.parse_args()
    main(args.truth_input,
         args.catfish_input, args.input, args.mode)
