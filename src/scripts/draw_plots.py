#!/usr/bin/python3
import argparse
import os
from src.scripts import io_helper
import pandas as pd

def main(input_folder):
    l = []
    print(input_folder)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            filename = f'{root}/{file}'
            l.append(pd.read_csv(filename))
    df = pd.concat(l)
    groups = df.groupby('number_of_paths_truth')
    for key, group in groups:
        print(key, len(group))
    print(groups['precision'].mean())
    print(groups['max_cov_rel'].mean())
    print(groups['number_of_paths'].sum())
    print(groups['paths_length_sum'].mean())
    print(groups.mean().to_csv())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    args = parser.parse_args()
    main(args.input_folder)
