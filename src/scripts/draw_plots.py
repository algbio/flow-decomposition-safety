#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from math import log2, log10
sns.set()

def main():
    catfish_df = pd.read_csv('catfish_summary' )
    safety_df = pd.read_csv('safety_summary' )

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['number_of_paths_truth'], catfish_df['precision'])
    plt.scatter(safety_df['number_of_paths_truth'], safety_df['precision'])
    plt.title('Precision')
    plt.ylabel('')
    plt.xlabel('')
    plt.savefig('precision.png')

    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['number_of_paths_truth'], catfish_df['max_cov_rel'])
    plt.scatter(safety_df['number_of_paths_truth'], safety_df['max_cov_rel'])
    plt.title('')
    plt.ylabel('')
    plt.xlabel('')
    plt.savefig('maximumcoverage.png')

    r = catfish_df['max_cov_rel']
    p = catfish_df['precision']
    plt.figure(figsize=(10,10))
    plt.scatter(catfish_df['number_of_paths_truth'], 2*(p*r)/(p+r))
    r = safety_df['max_cov_rel']
    p = safety_df['precision']
    plt.scatter(safety_df['number_of_paths_truth'], 2*(p*r)/(p+r))
    plt.title('Z-score')
    plt.ylabel('')
    plt.xlabel('')
    plt.savefig('zscore.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ic", "--input_folder_catfish")
    parser.add_argument("-is", "--input_folder_safety")
    args = parser.parse_args()
    main()
