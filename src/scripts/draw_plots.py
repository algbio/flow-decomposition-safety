#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from math import log2, log10
sns.set()

def main():
    catfish_df = pd.read_csv('summary/catfish/summary_seq.csv')
    safety_df = pd.read_csv('summary/safety/summary_seq.csv')
    munitigs_df = pd.read_csv("summary/modified_unitigs/summary_seq.csv")
    unitigs_df = pd.read_csv("summary/unitigs/summary_seq.csv")

    # average sequence length
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['avg_path_length'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['avg_path_length'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['avg_path_length'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['avg_path_length'], label='modified unitigs')
    plt.title('Average sequence length')
    plt.ylabel('Average length of seq')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/seq_length.png')

    #TODO: average length in nodes

    # max_cor_rel_bases_mean
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['max_cov_rel_bases_mean'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['max_cov_rel_bases_mean'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['max_cov_rel_bases_mean'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['max_cov_rel_bases_mean'], label='modified unitigs')
    plt.title('max_cov_rel_bases mean')
    plt.ylabel('max_cov_rel_bases')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/max_cov_rel_bases_mean.png')

    # max cov rel vertex
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['max_cov_rel_vertex_mean'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['max_cov_rel_vertex_mean'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['max_cov_rel_vertex_mean'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['max_cov_rel_vertex_mean'], label='modified unitigs')
    plt.title('max_cov_rel_vertex_mean')
    plt.ylabel('max_cov_rel_vertex')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/max_cov_rel_vertex_mean.png')

    # e size relative bases mean
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['e_size_rel_bases_mean'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['e_size_rel_bases_mean'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['e_size_rel_bases_mean'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['e_size_rel_bases_mean'], label='modified unitigs')
    plt.title('e_size_rel_bases_mean')
    plt.ylabel('e_size_rel_bases')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/e_sizes_re_bases_mean.png')

    # e sizes relative vertecies
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['e_sizes_rel_vertex_mean'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['e_sizes_rel_vertex_mean'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['e_sizes_rel_vertex_mean'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['e_sizes_rel_vertex_mean'], label='modified unitigs')
    plt.title('e_sizes_rel_vertex_mean')
    plt.ylabel('e_sizes_rel_vertex')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/max_cov_rel_vertex_mean.png')

    # vertex precision
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['vertex_precision'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['vertex_precision'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['vertex_precision'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['vertex_precision'], label='modified unitigs')
    plt.ylim(-0.01,1.1)
    plt.title('Weighted vertex precision')
    plt.ylabel('vertex precision')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/vertex_precision.png')

    # precision
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['precision'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['precision'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['precision'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['precision'], label='modified unitigs')
    plt.ylim(-0.01,1.1)
    plt.title('Precision')
    plt.ylabel('precision')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/precision.png')

    #base precision
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['base_precision'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['base_precision'], label='safety')
    plt.scatter(unitigs_df['k'], unitigs_df['base_precision'], label='unitigs')
    plt.scatter(munitigs_df['k'], munitigs_df['base_precision'], label='modified unitigs')
    plt.ylim(-0.01,1.1)
    plt.title('Weighted bases precision')
    plt.ylabel('precision')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/base_precision.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['fscore_bases'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['fscore_bases'], label='safety')
    plt.scatter(safety_df['k'], unitigs_df['fscore_bases'], label='unitigs')
    plt.scatter(safety_df['k'], munitigs_df['fscore_bases'], label='modified unitigs')
    plt.title('F-score (unweighted precision) bases')
    plt.ylabel('F-score bases')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/fscore_unweight_bases.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['fscore_vertex'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['fscore_vertex'], label='safety')
    plt.scatter(safety_df['k'], unitigs_df['fscore_vertex'], label='unitigs')
    plt.scatter(safety_df['k'], munitigs_df['fscore_vertex'], label='modified unitigs')
    plt.title('F-score (unweighted precision) vertex')
    plt.ylabel('F-score vertex')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/fscore_unweight_vertex.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['fscore_vertex_weighted'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['fscore_vertex_weighted'], label='safety')
    plt.scatter(safety_df['k'], unitigs_df['fscore_vertex_weighted'], label='unitigs')
    plt.scatter(safety_df['k'], munitigs_df['fscore_vertex_weighted'], label='modified unitigs')
    plt.title('F-score (weighted precision) vertex')
    plt.ylabel('F-score vertex')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/fscore_weight_vertex.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['fscore_bases_weighted'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['fscore_bases_weighted'], label='safety')
    plt.scatter(safety_df['k'], unitigs_df['fscore_bases_weighted'], label='unitigs')
    plt.scatter(safety_df['k'], munitigs_df['fscore_bases_weighted'], label='modified unitigs')
    plt.title('F-score (weighted precision) bases')
    plt.ylabel('F-score bases')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('plots/fscore_weight_bases.png')

if __name__ == '__main__':
    main()
