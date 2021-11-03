#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from math import log2, log10
sns.set()

def main(paths, order):
    bound1 = 2
    bound2 = 15
    base_cols = ["max_cov_rel_bases", "e_size_rel_bases", 
    "base_precision", "fscore_bases_weighted_esr", 
    "fscore_bases_weighted_mcv"]
    vertex_cols = ["max_cov_rel_vertex", "e_sizes_rel_vertex", 
    "vertex_precision", "fscore_vertex_weighted_esr", 
    "fscore_vertex_weighted_mcv"]
    all_dataframes = []
    for p in paths:
        all_dataframes.append(read_file(p))
    
    print('bases:')
    compute_values(all_dataframes, bound1, bound2, base_cols, order)
    print()
    print('vertex:')
    compute_values(all_dataframes, bound1, bound2, vertex_cols, order)

def compute_values(dfs, b1, b2, cols, order):
    print(f'k >= 2')
    stuff_a = []
    for df in dfs:
        a = df[(df.k >= b1)]
        print(f'{"{:.2f}".format(a.count()[0] / df.count()[0])}')
        l_a = [f'{"{:.2f}".format(a[c].mean())}' for c in cols]
        stuff_a.append(l_a)
    print_np_array_as_latex_table(stuff_a, order)
    stuff_a = []
    print(f'{b1} <= k <= {b2}')
    for df in dfs:
        a = df[(df.k>= b1) & (df.k <= b2)]
        print(f'{"{:.2f}".format(a.count()[0] / df.count()[0])}')
        l_a = [f'{"{:.2f}".format(a[c].mean())}' for c in cols]
        stuff_a.append(l_a)
    print_np_array_as_latex_table(stuff_a, order)
    stuff_a = []
    print(f'k>{b2}')
    for df in dfs:
        a = df[(df.k > b2)]
        print(f'{"{:.2f}".format(a.count()[0] / df.count()[0])}')
        l_a = [f'{"{:.2f}".format(a[c].mean())}' for c in cols]
        stuff_a.append(l_a)
    print_np_array_as_latex_table(stuff_a, order)


def print_np_array_as_latex_table(a, order):
    for i,o in enumerate(order):
        print("& " + o + " & " + "\\\\\n".join([" & ".join(a[i])]) + "\\\\")
    #print("\\\\\n".join([" & ".join(map(str, line)) for line in a]))
#

def read_file(input_folder):
    column_strings = ['e_sizes_rel_vertex', 'e_size_rel_bases', 'max_cov_rel_vertex', 'max_cov_rel_bases']
    l = []
    for root, dirs, files in os.walk(input_folder):
        # = root.split('/')[-1]
        if not dirs:
            for fi in files:
                filename= f'{root}/{fi}'
                try:
                    df = pd.read_json(filename)
                except ValueError:
                    continue
                for c in column_strings:
                    df[c] = [sum(x) for x in df[c]] / df['number_of_paths']
                l.append(df)
        else:
            for d in dirs:
                for r, d2, f in os.walk(f'{root}{d}'):
                    for fi in f:
                        filename= f'{r}/{fi}'
                        try:
                            df = pd.read_json(filename)
                        except ValueError:
                            continue
                        for c in column_strings:
                            df[c] = [sum(x) for x in df[c]] / df['number_of_paths']
                        l.append(df)
    df = pd.concat(l)
    return df[(df.k>=2)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish", default=None)
    parser.add_argument("-s", "--safety", default=None)
    parser.add_argument("-u", "--unitigs", default=None)
    parser.add_argument("-mu", "--modified_unitigs", default=None)
    parser.add_argument("-save", "--save", default=True)
    args = parser.parse_args()
    paths = []
    order = []
    if args.safety:
        paths.append(args.safety)
        order.append('Safe and Complete')
    if args.catfish:
        paths.append(args.catfish)
        order.append('Catfish')
    if args.unitigs:
        paths.append(args.unitigs)
        order.append('Unitigs')
    if args.modified_unitigs:
        paths.append(args.modified_unitigs)
        order.append('Extended Unitigs')
    main(paths, order)
