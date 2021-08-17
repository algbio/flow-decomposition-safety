#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from math import log2, log10
sns.set()

def main():
    catfish_df = pd.read_csv('../summary/catfish.csv')
    safety_df = pd.read_csv('../summary/safety.csv')
    mod_uni_df = pd.read_csv("../summary/modified_unitigs.csv")
    uni_df = pd.read_csv("../summary/unitigs.csv")

    plt.figure(figsize=(10,10))
    plt.scatter(safety_df['k'], safety_df['graphs_per_k'], label='catfish', c='navy')
    plt.title('Number of graphs size k')
    plt.ylabel('k')
    plt.xlabel('number of graphs')
    plt.savefig('number_of_graphs.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['avg_path_length'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['avg_path_length'], label='safety')
    plt.scatter(uni_df['k'], uni_df['avg_path_length'], label='unitigs')
    plt.scatter(mod_uni_df['k'], mod_uni_df['avg_path_length'], label='modified unitigs')
    plt.title('')
    plt.ylabel('Average lenngth of path')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('length.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], catfish_df['precision'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['precision'], label='safety')
    plt.title('')
    plt.ylabel('Precision')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('precision.png')

    plt.figure(figsize=(10,10))
    plt.ylim(0, 1.1)
    plt.scatter(catfish_df['k'], catfish_df['max_cov_rel'], label='catfish')
    plt.scatter(safety_df['k'], safety_df['max_cov_rel'], label='safety')
    plt.title('')
    plt.ylabel('max-cov-rel')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('max-cov-rel.png')

    r = catfish_df['max_cov_rel']
    p = catfish_df['precision']
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['k'], 2*(p*r)/(p+r), label='catfish')
    r = safety_df['max_cov_rel']
    p = safety_df['precision']
    plt.scatter(safety_df['k'], 2*(p*r)/(p+r), label='safety')
    plt.title('')
    plt.ylabel('F-score')
    plt.xlabel('k')
    plt.legend()
    plt.savefig('zscore.png')


if __name__ == '__main__':
    main()
