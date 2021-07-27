'''
Comparing safety or catfish result to truth file
'''
#!/usr/bin/python3
import argparse
from src.scripts import io_helper

def main(truth, output, catfish=None, safety=None):
    '''
    Main method for comparing graphs files. Outputs a file where
    each comparison result of graph pair is reported.
    Get paths to truth and output files as a parameter.
    Also either path to cafish or safety graph is given as a parameter.
    '''

    graphs1 = io_helper.read_file(catfish, 'catfish') if catfish else io_helper.read_file(safety, 'safety')

    graphs2 = io_helper.read_file(truth, 'truth')

    n = 0
    if len(graphs1) == len(graphs2):
        n = len(graphs1)
    else:
        print('graphs don\'t match. comparison can\'t be done')
        return
    io_helper.write_file(
        ',graph number,dataset,type,numer of paths,path flows\n', f'{output}.csv')
    for i in range(0, n):
        precision_value = precision(graphs1[i], graphs2[i])
        max_cov_rel_value = max_cov_rel(graphs[i], truth_graphs[i])
        n_paths = len(graphs[i])
        sum = 0
        for p in graphs[i]:
            sum += len(p)
        write_file(f'graph {i}', args.output_file)
        write_file(
            f'number_of_paths_in_truth_graph {len(truth_graphs[i])}', args.output_file)
        write_file(f'precision {precision_value}', args.output_file)
        write_file(f'max_cov_rel {max_cov_rel_value}', args.output_file)
        write_file(f'n_paths {n_paths}', args.output_file)
        write_file(f'avg_path_length {average_path_length(graphs[i])}', args.output_file)
        write_file(
            f'number_of_paths_in_truth_graph {len(truth_graphs[i])}', args.output_file)
        write_file(f'n_paths {n_paths}', args.output_file)
        write_file(f'sum_of_path_lengths {sum}', args.output_file)
# returns how many graph paths were included in truth graph paths
# path is included if it is contained as a whole in (some) truth path


def precision(graph, truth_graph):
    included = 0
    number_of_paths = len(graph)
    for path in graph:
        for true_path in truth_graph:
            if correct(path, true_path):
                included += 1
                break
    return included/number_of_paths


def correct(path, truth_path):
    return str(path)[1:-1] in str(truth_path)

# for each path in truth graph best overlap of graph path is calculated
# overlapping fractions for each truth path are added together in variable total
# total is then divided by number of paths in truth graph and returned
# returns average of best graph path overlaps of truth graph paths


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


def average_path_length(graph):
    n = len(graph)
    total = 0
    for path in graph:
        total += len(path)
    return total/n


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str} \n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish_input", default=None)
    parser.add_argument("-s", "--safety_input", default=None)
    parser.add_argument("-t", "--truth_input", default=None)
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    main(args.truth_input, args.output_file, args.catfish_input, args.safety_input)
