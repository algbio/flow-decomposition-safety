'''
Converts sgr/graph file to gfa file.
'''

#!/usr/bin/python3
import argparse
import networkx as nx
from src.scripts import io_helper

def main(filename):
    graphs = io_helper.read_sg_file(filename)
    j = 0
    index_dic = {}
    for graph in graphs:
        i = 1
        for n in graph.nodes:
            if n != '(0,0)' and n!='(-1,-1)':
                graph.nodes[n]['index'] = i
                index_dic[i] = n
                i += 1
        graph.nodes['(0,0)']['index'] = 0
        graph.nodes['(-1,-1)']['index'] = len(graph.nodes)-1
        index_dic[0] = '0,0'
        index_dic[len(graph.nodes)-1] = '(-1,-1)'
        print(f'# graph {j} {index_dic}')
        print(len(graph.nodes))
        for n1,n2,w in graph.edges(data=True):
            
            print(f'{graph.nodes[n1]["index"]} {graph.nodes[n2]["index"]} {w["weight"]}')
        j+=1
        index_dic = {}
                  
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--file", help="path to file")
    args = parser.parse_args()
    main(args.file)
