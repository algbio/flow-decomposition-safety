'''
Draws a summary from datafolder given as a parameter.
TODO: probably redundant, will be included to plotting file?
'''
#!/usr/bin/python3
import argparse
import os
from src.scripts import io_helper
import pandas as pd

def main(input_folder, output):
    '''
    Gets input folder and output file as a parameter.
    Outputs a csv-file containing summary of the data.
    TODO: at to moment output file doesn't really make sense.
    Will be fixed/this will be removed before plotting the results next time.
    '''
   
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
    io_helper.write_file(groups.mean().to_csv(),output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-o", "--output_file")
    args = parser.parse_args()
    main(args.input_folder, args.output_file)
