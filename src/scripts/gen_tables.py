#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as npf
import pandas as pd
from math import log2, log10
sns.set()

def main(cat_path, safety_path, unitigs_path, save):
    bound1 = 2
    bound2 = 15
    
    if safety_path:
        safety_df = pd.read_csv(safety_path)
    else:
        safety_df = None
    if cat_path:
        cat_df = pd.read_csv(cat_path)
    else:
        cat_df = None
    if unitigs_path:
        unitigs_df = pd.read_csv(unitigs_path)
    else:
        unitigs_df = None
    saf_pre = precentage(safety_df, bound1, bound2)
    cat_pre = precentage(cat_df, bound1, bound2)
    uni_pre = precentage(unitigs_df, bound1, bound2)
    print(f'k>={bound1}')
    print('bases')
    print(table_string_bases(safety_df[safety_df.k>= bound1], cat_df[cat_df.k>= bound1], unitigs_df[unitigs_df.k>= bound1]))
    print('vertex')
    print(table_string_vertex(safety_df[safety_df.k>= bound1], cat_df[cat_df.k>= bound1], unitigs_df[unitigs_df.k>= bound1]))
    print(f'{"{:.2f}".format(saf_pre[0])}')
    print(f'{"{:.2f}".format(cat_pre[0])}')
    print(f'{"{:.2f}".format(uni_pre[0])}')

    print(f'{bound1}<= k =< {bound2}')
    print('bases')
    print(table_string_bases(safety_df[(safety_df.k>= bound1) & (safety_df.k <= bound2)], cat_df[(cat_df.k>= bound1) & (cat_df.k <= bound2)], unitigs_df[(unitigs_df.k>= bound1) & (unitigs_df.k <= bound2)]))
    print('vertex')
    print(table_string_vertex(safety_df[(safety_df.k>= bound1) & (safety_df.k <= bound2)], cat_df[(cat_df.k>= bound1) & (cat_df.k <= bound2)], unitigs_df[(unitigs_df.k>= bound1) & (unitigs_df.k <= bound2)]))
    print(f'{"{:.2f}".format(saf_pre[1])}')
    print(f'{"{:.2f}".format(cat_pre[1])}')
    print(f'{"{:.2f}".format(uni_pre[1])}')

    print(f'k > {bound2}')
    print('bases')
    print(table_string_bases(safety_df[safety_df.k > bound2], cat_df[cat_df.k > bound2], unitigs_df[unitigs_df.k > bound2]))
    print('vertex')
    print(table_string_vertex(safety_df[safety_df.k > bound2], cat_df[cat_df.k > bound2], unitigs_df[unitigs_df.k > bound2]))
    print(f'{"{:.2f}".format(saf_pre[2])}')
    print(f'{"{:.2f}".format(cat_pre[2])}')
    print(f'{"{:.2f}".format(uni_pre[2])}')

def table_string_bases(safety_df, cat_df, unitigs_df):
    return f'''& Safe and Complete &  {"{:.2f}".format(safety_df.mean()["max_cov_rel_bases_mean"])} & {"{:.2f}".format(safety_df.mean()["e_size_rel_bases_mean"])} & {"{:.2f}".format(safety_df.mean()["base_precision"])} & {"{:.2f}".format(safety_df.mean()["fscore_bases_weighted_esr"])} & {"{:.2f}".format(safety_df.mean()["fscore_bases_weighted_mcv"])} \\\\
& Catfish & {"{:.2f}".format(cat_df.mean()["max_cov_rel_bases_mean"])} & {"{:.2f}".format(cat_df.mean()["e_size_rel_bases_mean"])} & {"{:.2f}".format(cat_df.mean()["base_precision"])} & {"{:.2f}".format(cat_df.mean()["fscore_bases_weighted_esr"])} & {"{:.2f}".format(cat_df.mean()["fscore_bases_weighted_mcv"])} \\\\
& Unitigs& {"{:.2f}".format(unitigs_df.mean()["max_cov_rel_bases_mean"])} & {"{:.2f}".format(unitigs_df.mean()["e_size_rel_bases_mean"])} & {"{:.2f}".format(unitigs_df.mean()["base_precision"])} & {"{:.2f}".format(unitigs_df.mean()["fscore_bases_weighted_esr"])} & {"{:.2f}".format(unitigs_df.mean()["fscore_bases_weighted_mcv"])} \\\\'''
def table_string_vertex(safety_df, cat_df, unitigs_df):
    return f'''& Safe and Complete &  {"{:.2f}".format(safety_df.mean()["max_cov_rel_vertex_mean"])} & {"{:.2f}".format(safety_df.mean()["e_sizes_rel_vertex_mean"])} & {"{:.2f}".format(safety_df.mean()["vertex_precision"])} & {"{:.2f}".format(safety_df.mean()["fscore_vertex_weighted_esr"])} & {"{:.2f}".format(safety_df.mean()["fscore_vertex_weighted_mcv"])} \\\\
& Catfish & {"{:.2f}".format(cat_df.mean()["max_cov_rel_vertex_mean"])} & {"{:.2f}".format(cat_df.mean()["e_sizes_rel_vertex_mean"])} & {"{:.2f}".format(cat_df.mean()["vertex_precision"])} & {"{:.2f}".format(cat_df.mean()["fscore_vertex_weighted_esr"])} & {"{:.2f}".format(cat_df.mean()["fscore_vertex_weighted_mcv"])} \\\\
& Unitigs& {"{:.2f}".format(unitigs_df.mean()["max_cov_rel_vertex_mean"])} & {"{:.2f}".format(unitigs_df.mean()["e_sizes_rel_vertex_mean"])} & {"{:.2f}".format(unitigs_df.mean()["vertex_precision"])} & {"{:.2f}".format(unitigs_df.mean()["fscore_vertex_weighted_esr"])} & {"{:.2f}".format(unitigs_df.mean()["fscore_vertex_weighted_mcv"])} \\\\'''

def precentage(df,b1,b2):
    return(sum(df[df.k>= b1].number_of_graphs_per_k) / sum(df.number_of_graphs_per_k),
     sum(df[(df.k>= b1) & (df.k <= b2)].number_of_graphs_per_k) / sum(df.number_of_graphs_per_k), 
     sum(df[df.k >= b2].number_of_graphs_per_k) / sum(df.number_of_graphs_per_k))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish", default=None)
    parser.add_argument("-s", "--safety", default=None)
    parser.add_argument("-u", "--unitigs", default=None)
    parser.add_argument("-mu", "--modified_unitigs", default=None)
    parser.add_argument("-save", "--save", default=True)
    args = parser.parse_args()
    main(args.catfish, args.safety, args.unitigs, args.save)
