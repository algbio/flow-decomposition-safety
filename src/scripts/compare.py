'''
Comparing safety or catfish result to truth file
'''
#!/usr/bin/python3
import argparse
import numpy as np
from src.scripts import io_helper
import csv
from sys import stdout

def main(truth, catfish=None, comp=None):
    '''
    Main method for comparing graphs files. Outputs 
    each comparison result for compared graphs is reported.
    '''
    graphs = io_helper.read_file(catfish, 'catfish') if catfish else io_helper.read_file(comp)

    truth_graphs = io_helper.read_file(truth, 'truth')
    n = 0
    if len(graphs) == len(truth_graphs):
        n = len(truth_graphs)
    else:
        print('graphs don\'t match. comparison can\'t be done')
        return
    writer = csv.writer(stdout)
    
    writer.writerow(['graph',
    'e_size_rel_vertex',
    'max_cov_rel_vertex',
    'precision',
    'vertex_precision',
    'k',
    'node_sum'
    'number_of_paths',
    'fscore_vertex',
    'fscore_vertex_weighted'])
    for i in range(0, n):
        writer.writerow([i,#graph
               compute_e_size_rel(truth_graphs[i], graphs[i]), #e-size-rel
               max_cov_rel(graphs[i], truth_graphs[i]),#max-cov-rel
               precision(graphs[i], truth_graphs[i]),#pre
               0, #vertex precision
               len(truth_graphs[i]),#k
               0, # node sum
               len(graphs[i]),#number of paths
               0, #f-score-vertex
               0 #fscore-vertex-weighted
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

def compute_e_size_rel(transcript_paths, contigs):
    contigs_through = dict()
    ## For every vertex in a contig, compute the contigs using that vertex and its index in the corresponding contig
    for c, contig in enumerate(contigs):
        for i, v in enumerate(contig):
            if contigs_through.get(v, None) is None:
                contigs_through[v] = list()
            contigs_through[v].append((c,i))
    
    e_size_per_transcript_path = list()
    e_size_per_transcript_path_vertex = list()
    for transcript_path in transcript_paths:
        
        length = 0
        e_sum = 0
        e_sum_vertex = 0
        for j, v in enumerate(transcript_path):
            #exon_length = interval_length(v)
            #length += exon_length
            
            if contigs_through.get(v, None) is not None:
                total_length_intersections = 0
                total_length_intersections_vertex = 0
                
                for c,i in contigs_through[v]:
                    
                    contig = contigs[c]
                    l_p = i
                    while l_p >= 0 and (j-(i-l_p)) >= 0 and contig[l_p] == transcript_path[(j-(i-l_p))]:
                        l_p -= 1
                    
                    l_p += 1
                    
                    r_p = i
                    while r_p < len(contig) and (j-(i-r_p)) < len(transcript_path) and contig[r_p] == transcript_path[(j-(i-r_p))]:
                        r_p += 1
                    r_p -= 1
                    
                    intersection = contig[l_p:r_p+1]
                    #total_length_intersections += base_length(intersection)
                    total_length_intersections_vertex += len(intersection)
                    
                    
                #e_sum += exon_length*(total_length_intersections/len(contigs_through[v]))
                e_sum_vertex += total_length_intersections_vertex/len(contigs_through[v])
                    
                
        #e_size_per_transcript_path.append(e_sum/(length*length))
        e_size_per_transcript_path_vertex.append(e_sum_vertex/(len(transcript_path)*len(transcript_path)))
    
    return sum(e_size_per_transcript_path_vertex)/len(contigs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish_input", default=None)
    parser.add_argument("-i", "--input", default=None)
    parser.add_argument("-t", "--truth_input")
    parser.add_argument('-m','--mode', default=None)
    args = parser.parse_args()
    main(args.truth_input,
         args.catfish_input, args.input, args.mode)
