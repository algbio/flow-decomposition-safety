#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from math import log2, log10
sns.set()

def main(paths, save, path):
    #plt.rcParams.update({'font.size': 53})
    fontsize = 22
    plt.rc('xtick', labelsize=fontsize) 
    plt.rc('ytick', labelsize=fontsize) 
    dframes = []
    for p in paths:
        df = pd.read_csv(p)
        df.name = p.split('/')[1].replace('_',' ').replace('And','&')
        #df.name = p.replace('_',' ')
        dframes.append(df)
    # figure parameters
    columns = [
                'max_cov_rel_bases_avg', 'max_cov_rel_vertex_avg', 
                'e_size_rel_bases_avg', 'e_sizes_rel_vertex_avg',
                'vertex_precision', 'precision','base_precision', 
                'fscore_bases_mcv', 'fscore_vertex_mcv',
                'fscore_vertex_weighted_mcv','fscore_bases_weighted_mcv',
                'fscore_bases_esr', 'fscore_vertex_esr',
                'fscore_vertex_weighted_esr','fscore_bases_weighted_esr'
                ]
    titles = [
                'Average sequence length', 'Average path length (vertices)',
                'Maximum relative coverage bases', 'Maximum relative coverage vertices',
                'E-size relative bases', 'E-size_relative vertices',
                'Weighted vertex precision', 'Precision', 'Weighted bases precision',
                'F-score (unweighted precision, max-rel-cov) bases', 'F-score (unweighted precision, max-rel-cov) vertices',
                'F-score (weighted precision, max-rel-cov) bases', 'F-score (weighted precision, max-rel-cov) vertices',
                'F-score (unweighted precision, e-size-rel) bases', 'F-score (unweighted precision, e-size-rel) vertices',
                'F-score (weighted precision, e-size-rel) bases', 'F-score (weighted precision, e-size-rel) vertices',
                ]
    for i,col in enumerate(columns):
        plt.figure(figsize=(10,10))
        for df in dframes:
            plt.scatter(df['k'], df[col], label=df.name)
            #plt.scatter(df['k'], df[col])
        #plt.title(titles[i])
        # plt.ylabel()
        plt.xlabel('k', fontsize=fontsize)
        plt.legend(fontsize=fontsize)
        if save:
            plt.savefig(f'{path}/{col}.png')
        else:
            plt.show()
    return 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--catfish", default=None)
    parser.add_argument("-s", "--safety", default=None)
    parser.add_argument("-u", "--unitigs", default=None)
    parser.add_argument("-mu", "--modified_unitigs", default=None)
    parser.add_argument("-save", "--save", default=True)
    parser.add_argument("-p", "--path", default='plots')
    args = parser.parse_args()
    paths = []

    if args.unitigs:
        paths.append(args.unitigs)
    if args.modified_unitigs:
        paths.append(args.modified_unitigs)
    if args.safety:
        paths.append(args.safety)
    if args.catfish:
        paths.append(args.catfish)
    
    
    
    main(paths, args.save, args.path)
