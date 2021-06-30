#!/usr/bin/python3
import argparse
import os
import io_helper
from timeit import default_timer as timer
import matplotlib.pyplot as plt
import networkx as nx
from graph import Graph


def main():
    '''
    G = nx.DiGraph()
    G.add_edges_from(
        [(8, 14, {'capacity': 5}),
         (2, 3, {'capacity': 1}),
         (3, 4, {'capacity': 6}),
         (5, 9, {'capacity': 1}),
         (5, 6, {'capacity': 5}),
         (9, 10, {'capacity': 1}),
         (11, 12, {'capacity': 1}),
         (12, 13, {'capacity': 1}),
         (10, 11, {'capacity': 1}),
         (13, 14, {'capacity': 1}),
         (0, 1, {'capacity': 5}),
         (0, 2, {'capacity': 1}),
         (1, 3, {'capacity': 5}),
         (4, 5, {'capacity': 6}),
         (6, 7, {'capacity': 5}),
         (7, 8, {'capacity': 5})])
    G.nodes[0]['flow_in'] = 0
    G.nodes[0]['flow_out'] = 6
    G.nodes[1]['flow_in'] = 5
    G.nodes[1]['flow_out'] = 5
    G.nodes[6]['flow_in'] = 5
    G.nodes[6]['flow_out'] = 5
    G.nodes[7]['flow_in'] = 5
    G.nodes[7]['flow_out'] = 5
    G.nodes[8]['flow_in'] = 5
    G.nodes[8]['flow_out'] = 5
    G.nodes[2]['flow_in'] = 1
    G.nodes[2]['flow_out'] = 1
    G.nodes[9]['flow_in'] = 1
    G.nodes[9]['flow_out'] = 1
    G.nodes[10]['flow_in'] = 1
    G.nodes[10]['flow_out'] = 1
    G.nodes[11]['flow_in'] = 1
    G.nodes[11]['flow_out'] = 1
    G.nodes[12]['flow_in'] = 1
    G.nodes[12]['flow_out'] = 1
    G.nodes[13]['flow_in'] = 1
    G.nodes[13]['flow_out'] = 1
    G.nodes[3]['flow_in'] = 6
    G.nodes[3]['flow_out'] = 6
    G.nodes[4]['flow_in'] = 6
    G.nodes[4]['flow_out'] = 6
    G.nodes[5]['flow_in'] = 6
    G.nodes[5]['flow_out'] = 6
    G.nodes[14]['flow_in'] = 6
    G.nodes[14]['flow_out'] = 0
    print(G.edges(data=True))
    print(G.nodes(data=True))
    g = Graph(G, 0, 14)
    # test_max_safe_apths(g)
    #pos = nx.spiral_layout(G)
    #nx.draw(G, pos)
    #labels = nx.get_edge_attributes(G, 'capacity')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    #plt.show()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-safety", "--safety_input")
    parser.add_argument("-truth", "--truth_input")
    parser.add_argument("-o", "--output_file",)
    args = parser.parse_args()
    test_files(args.safety_input, args.truth_input, args.output_file)

def test_files(safety, truth, output):
    safety_graphs = io_helper.read_file(safety)
    truth_graphs = io_helper.read_file(truth)
    n = len(safety_graphs)
    for i in range(0, n):
        io_helper.write_file(f'graph {i}', output)
        safety_paths = safety_graphs[i]
        truth_paths = truth_graphs[i]
        subpath = False
        for safe_path in safety_paths:
            for truth_path in truth_paths:
                if str(safe_path)[1:-1] in str(truth_path):
                    io_helper.write_file(f'pass', output)
                    subpath = True
                    break
            if not subpath:
                io_helper.write_file(f'fail', output)
                io_helper.write_file(f'{safe_path}', output)
            subpath = False



def test_flow_decomposition(graph):
    comp = graph.flow_decomposition()
    print(comp)
    print(graph)

def test_max_safe_apths(graph):
    comp = graph.flow_decomposition()
    print(comp)
    print(graph)
    max = graph.maximal_safe_paths()
    print(max)
    print(graph)


if __name__ == '__main__':
    main()
