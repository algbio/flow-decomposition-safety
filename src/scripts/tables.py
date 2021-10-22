#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as npf
import pandas as pd
from math import log2, log10
sns.set()

def main(paths, save, path):
    dframes = []
    for p in paths:
        df = pd.read_csv(p)
        df.name = p.split('/')[1].replace('_',' ')
        dframes.append(df)
    # figure parameters
    columns = [
                'avg_path_length_seq', 'avg_path_length_nodes', 
                'max_cov_rel_bases_mean', 'max_cov_rel_vertex_mean', 
                'e_size_rel_bases_mean', 'e_sizes_rel_vertex_mean',
                'vertex_precision', 'precision','base_precision', 
                'fscore_bases', 'fscore_vertex',
                'fscore_vertex_weighted','fscore_bases_weighted'
                ]
    titles = [
                'Average sequence length', 'Average path length (vertices)',
                'Maximum relative coverage bases', 'Maximum relative coverage vertices',
                'E-size relative bases', 'E-size_relative vertices',
                'Weighted vertex precision', 'Precision', 'Weighted bases precision',
                'F-score (unweighted precision) bases', 'F-score (unweighted precision) vertices',
                'F-score (weighted precision) bases', 'F-score (weighted precision) vertices',
                ]
    bound1 = 2
    bound2 = 15
    for df in dframes:
        print('vertex')
        lower = df[df.k <= bound1]
        print(f'& {df.name} & {"{:.2f}".format(lower.mean()["max_cov_rel_vertex_mean"])} '+
        f'& {"{:.2f}".format(lower.mean()["e_sizes_rel_vertex_mean"])} ' +
         f'& {"{:.2f}".format(lower.mean()["vertex_precision"])} ' +
         f'& {"{:.2f}".format(lower.mean()["fscore_vertex"])} '+
         f'& {"{:.2f}".format(lower.mean()["fscore_vertex_weighted"])} ' + 
         f'\\\\')

        middle = df[(df.k > bound1) & (df.k < bound2)]
        print(f'& {df.name} & {"{:.2f}".format(middle.mean()["max_cov_rel_vertex_mean"])} '+
        f'& {"{:.2f}".format(middle.mean()["e_sizes_rel_vertex_mean"])} ' +
         f'& {"{:.2f}".format(middle.mean()["vertex_precision"])} ' +
         f'& {"{:.2f}".format(middle.mean()["fscore_vertex"])} '+
         f'& {"{:.2f}".format(middle.mean()["fscore_vertex_weighted"])} ' + 
         f'\\\\')

        upper = df[df.k >= bound2]
        print(f'& {df.name} & {"{:.2f}".format(upper.mean()["max_cov_rel_vertex_mean"])} '+
        f'& {"{:.2f}".format(upper.mean()["e_sizes_rel_vertex_mean"])} ' +
         f'& {"{:.2f}".format(upper.mean()["vertex_precision"])} ' +
         f'& {"{:.2f}".format(upper.mean()["fscore_vertex"])} '+
         f'& {"{:.2f}".format(upper.mean()["fscore_vertex_weighted"])} ' + 
         f'\\\\')
        print('bases')
        print(f'& {df.name} & {"{:.2f}".format(lower.mean()["max_cov_rel_bases_mean"])} '+
        f'& {"{:.2f}".format(lower.mean()["e_size_rel_bases_mean"])} ' +
         f'& {"{:.2f}".format(lower.mean()["base_precision"])} ' +
         f'& {"{:.2f}".format(lower.mean()["fscore_bases"])} '+
         f'& {"{:.2f}".format(lower.mean()["fscore_bases_weighted"])} ' + 
         f'\\\\')

        print(f'& {df.name} & {"{:.2f}".format(middle.mean()["max_cov_rel_bases_mean"])} '+
        f'& {"{:.2f}".format(middle.mean()["e_size_rel_bases_mean"])} ' +
         f'& {"{:.2f}".format(middle.mean()["base_precision"])} ' +
         f'& {"{:.2f}".format(middle.mean()["fscore_bases"])} '+
         f'& {"{:.2f}".format(middle.mean()["fscore_bases_weighted"])} ' + 
         f'\\\\')

        print(f'& {df.name} & {"{:.2f}".format(upper.mean()["max_cov_rel_bases_mean"])} '+
        f'& {"{:.2f}".format(upper.mean()["e_size_rel_bases_mean"])} ' +
         f'& {"{:.2f}".format(upper.mean()["base_precision"])} ' +
         f'& {"{:.2f}".format(upper.mean()["fscore_bases"])} '+
         f'& {"{:.2f}".format(upper.mean()["fscore_bases_weighted"])} ' + 
         f'\\\\')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish", default=None)
    parser.add_argument("-s", "--safety", default=None)
    parser.add_argument("-u", "--unitigs", default=None)
    parser.add_argument("-mu", "--modified_unitigs", default=None)
    parser.add_argument("-save", "--save", default=True)
    parser.add_argument("-p", "--path", default='plots/')
    args = parser.parse_args()
    paths = []
    if args.catfish:
        paths.append(args.catfish)
    if args.unitigs:
        paths.append(args.unitigs)
    if args.modified_unitigs:
        paths.append(args.modified_unitigs)
    if args.safety:
        paths.append(args.safety)
    main(paths, args.save, args.path)
