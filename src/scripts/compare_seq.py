#!/usr/bin/python3
import argparse
import numpy as np
from json import dumps

def main(truth, catfish=None, comp=None, mode=None):
    
    if comp:
        res = read_res(comp)
    if catfish:
        res = read_res_catfish(catfish)
    truth = read_truth(truth)


    if len(truth) != len(res):
        print(len(truth))
        print(len(res))
        print(f'Error in, res and truth files have a different number of graphs, continuing to next dataset')
        return

    metrics = list()
    for i in range(len(truth)):
        truth_paths = list(map(lambda truth_path: truth_path['path'], truth[i]))
        res_paths = res[i]

        e_sizes_rel_vertex, e_size_rel_bases = compute_e_size_rel(truth_paths, res_paths)
        max_cov_rel_vertex, max_cov_rel_bases = max_covered_rel_by_a_contig(truth_paths, res_paths)
        precision, vertex_precision, base_precision = compute_precision(truth_paths, res_paths)
        metrics.append({
            'e_sizes_rel_vertex': to_float(e_sizes_rel_vertex),
            'e_size_rel_bases': to_float(e_size_rel_bases),
            'max_cov_rel_vertex': to_float(max_cov_rel_vertex),
            'max_cov_rel_bases': to_float(max_cov_rel_bases),
            'precision': precision,
            'vertex_precision': vertex_precision,
            'base_precision': base_precision,
            'k': len(truth_paths),
            'seq_length_sum': seq_length_sum(res_paths),
            'number_of_paths':len(res_paths),
            'fscore_vertex': f_scores(precision,to_float(max_cov_rel_vertex)),
            'fscore_bases':f_scores(precision,to_float(max_cov_rel_bases))
        })
    print(dumps(metrics, indent=4))

def f_scores(p, r):
    try:
        r_mean = sum(r)/len(r)
    except ZeroDivisionError:
        r_mean = 0
    
    try:
        f = 2*(p*r_mean)/(p+r_mean)
    except ZeroDivisionError:
        f = 0
    return f


def seq_length_sum(paths):
    sum = 0
    for p in paths:
        for t in p:
            if tuple(t) != (0,0) and tuple(t) != (-1,-1):
                sum += (tuple(t)[1] - tuple(t)[0])
    return sum

# Adapted from Milla's code
def read_truth(filename):
    
    graphs = list()
    graph = list()
    
    with open(filename, 'r') as f:
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = list()
            # File line is a path
            else:
                items = line.split()
                cov = float(items[0])
                path = list(map(lambda p_exon: (int(p_exon.split(',')[0][1:]), int(p_exon.split(',')[1][:-1])), items[1:]))
                graph.append({
                    'path': path,
                    'cov': cov
                })
    graphs.append(graph)
    return graphs

def read_res_catfish(filename):
    
    graphs = list()
    graph = list()
    
    with open(filename, 'r') as f:
        node_dic = {}
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                node_dic = eval(' '.join(line.split()[3:-3]))
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = list()
            # File line is a path
            else:
                parts = line.split()
                path = [int(x) for x in parts[1:]]
                fpath = []
                for i in range(0,len(path)):
                    fpath.append(node_dic[path[i]])
                graph.append([eval(x) for x in fpath])
                
                
    graphs.append(graph)
    return graphs
'''
# Adapted from Milla's code (too)
def read_res_catfish(filename):
    
    graphs = list()
    graph = list()
    
    with open(filename, 'r') as f:
        node_dic = {}
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                parts = line.split()
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = list()
            # File line is a path
            else:
                graph.append(list(map(lambda p_exon: (int(p_exon.split(',')[0][1:]), int(p_exon.split(',')[1][:-1])), line.split())))
                
    graphs.append(graph)
    return graphs
'''
# Adapted from Milla's code (too)
def read_res(filename):
    
    graphs = list()
    graph = list()
    
    with open(filename, 'r') as f:
        for line in f:
            # Hashtag(#) begins a graph defenition in file
            if line[0] == '#':
                if len(graph) > 0:
                    graphs.append(graph)
                    graph = list()
            # File line is a path
            else:
                graph.append(list(map(lambda p_exon: (int(p_exon.split(',')[0][1:]), int(p_exon.split(',')[1][:-1])), line.split())))
                
    graphs.append(graph)
    return graphs

def interval_length(interval):
    return interval[1]-interval[0]+1

## It computes the base length of a transcript
def base_length(contig):
    length = 0
    for v in contig:
        length += interval_length(v)
    return length

## The e_size is computed for every transcript path, and for every base in this transcript path
## For every transcript EVERY contig intersecting with that contig is considered
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
            exon_length = interval_length(v)
            length += exon_length
            
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
                    total_length_intersections += base_length(intersection)
                    total_length_intersections_vertex += len(intersection)
                    
                    
                e_sum += exon_length*(total_length_intersections/len(contigs_through[v]))
                e_sum_vertex += total_length_intersections_vertex/len(contigs_through[v])
                    
                
        e_size_per_transcript_path.append(e_sum/(length*length))
        e_size_per_transcript_path_vertex.append(e_sum_vertex/(len(transcript_path)*len(transcript_path)))
    
    return e_size_per_transcript_path_vertex, e_size_per_transcript_path

## Returns a list t_p of size len(contigs) such that 
## tp[i] is true iff contigs[i] aligns completely to some
## transcript path
def true_positives(transcript_paths, contigs):
    t_p = [False]*len(contigs)
    
    contigs_staring_at = dict()
    ## For every start vertex in a contig, put the corresponding contig in the dict
    for c, contig in enumerate(contigs):
        v = contig[0]
        if contigs_staring_at.get(v, None) is None:
            contigs_staring_at[v] = list()
        contigs_staring_at[v].append(c)
    
    
    for transcript_path in transcript_paths:
        
        for i,v in enumerate(transcript_path):
            if contigs_staring_at.get(v, None) is not None:
                not_aligning_contigs = list()
                
                for c in contigs_staring_at[v]: ## All contigs evaluated start at some vertex of the transcript
                    contig = contigs[c]
                    if i+len(contig) <= len(transcript_path): ## They also end at some vertex of the contig
                        aligns = True
                        for j in range(len(contig)):
                            if contig[j] != transcript_path[j+i]:
                                aligns = False
                                break
                        if aligns:
                            t_p[c] = True
                        else:
                            not_aligning_contigs.append(c)
                    else:
                        not_aligning_contigs.append(c)
                
                contigs_staring_at[v] = not_aligning_contigs
    
    
    return t_p

## Returns the normal precision (#correts contigs/#contigs), 
## the vertex weighted precision (#sum vertices in correct contigs/#sum vertices in all contigs)
## and the base weigthed precision (#sum bases in correct contigs/#sum bases in all contigs)
def compute_precision(transcript_paths, contigs):
    tps = true_positives(transcript_paths, contigs)
    
    #True positives
    tp = 0
    tp_vertex = 0
    tp_bases = 0
    
    # Positives
    p = 0
    p_vertex = 0
    p_bases = 0
    
    for i, is_tp in enumerate(tps):
        contig = contigs[i]
        contig_base_length = base_length(contig)
        
        p += 1
        p_vertex += len(contig)
        p_bases += contig_base_length
        
        if is_tp:
            tp += 1
            tp_vertex += len(contig)
            tp_bases += contig_base_length
    try:
        x = 1.0*tp/p
    except ZeroDivisionError:
        x = 0
    try:
        y= 1.0*tp_vertex/p_vertex
    except ZeroDivisionError:
        y = 0
    try:
        z = 1.0*tp_bases/p_bases
    except ZeroDivisionError:
        z = 0
    return x,y,z
        
    

## Returns a list max_cov of length len(transcript_paths)
## such that max_cov[i] is the maximum of (vertices, bases)
## covered by any contig in contigs INTERSECTING to transcript_path[i]
def max_covered_rel_by_a_contig(transcript_paths, contigs):
    max_cov_vertex = list()
    max_cov_bases = list()
    
    contigs_through = dict()
    
    ## For every vertex in a contig, compute the contigs using that vertex and its index in the corresponding contig
    for c, contig in enumerate(contigs):
        for i, v in enumerate(contig):
            if contigs_through.get(v, None) is None:
                contigs_through[v] = list()
            contigs_through[v].append((c,i))
            
    
    for transcript_path in transcript_paths:
        max_bases = 0
        max_vertex = 0
        
        for j,v in enumerate(transcript_path):
            
            
            
            if contigs_through.get(v, None) is not None:
                
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
                    length_intersection_vertex = len(intersection)
                    length_intersection_bases = base_length(intersection)
                    
                    
                    
                    max_bases = max(max_bases, length_intersection_bases)
                    max_vertex = max(max_vertex, length_intersection_vertex)
                    
                    
                    
        max_cov_bases.append(max_bases/base_length(transcript_path))
        max_cov_vertex.append(max_vertex/len(transcript_path))
    
    return max_cov_vertex, max_cov_bases

## Compute and store the metrics to a json file in a list per graph.
def to_float(l):
    return list(map(lambda e: float(e), l))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish_input", default=None)
    parser.add_argument("-i", "--input", default=None)
    parser.add_argument("-t", "--truth_input")
    parser.add_argument('-m','--mode', default=None)
    args = parser.parse_args()
    main(args.truth_input,
         args.catfish_input, args.input, args.mode)
    