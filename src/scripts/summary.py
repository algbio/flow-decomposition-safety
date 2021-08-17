'''
Draws a summary from datafolder given as a parameter.
TODO: probably redundant, will be included to plotting file?
'''
#!/usr/bin/python3
import argparse
import os
from src.scripts import io_helper
import pandas as pd

def main(input_folder):
    '''
    Gets input folder as a parameter.
    Outputs a csv-file containing summary of the data.
    '''
    l = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            filename = f'{root}/{file}'
            l.append(pd.read_csv(filename))
    df = pd.concat(l)
    groups = df.groupby('k')
    sdf = groups.mean()[['precision', 'max_cov_rel']]
    sdf['avg_path_length'] = groups.sum()['path_length_sum'] / groups.sum()['number_of_paths']
    sdf['graphs_per_k'] = groups.count()['graph']
    print(sdf.to_csv())
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    args = parser.parse_args()
    main(args.input_folder)
