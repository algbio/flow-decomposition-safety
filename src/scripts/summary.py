'''
Draws a summary from datafolder given as a parameter.
'''
#!/usr/bin/python3
import argparse
import os
import pandas as pd

def main(input_folder):
    '''
    Gets input folder as a parameter.
    Outputs a csv-file containing summary of the data.
    '''
    l=[]
    for root, dirs, files in os.walk(input_folder):
        type = root.split('/')[-1]
        for file in files:
            filename = f'{root}/{file}'
            df = pd.read_csv(filename)
            l.append(df)
    df = pd.concat(l)

    groups = df.groupby('k')
    sdf = groups.mean()[['precision', 'max_cov_rel']]
    sdf['avg_path_length'] = groups.sum()['path_length_sum'] / groups.sum()['number_of_paths']
    sdf['graphs_per_k'] = groups.count()['graph']
    sdf['path_sum'] = groups.sum()['number_of_paths']
    sdf['paths_length_sum'] = groups.sum()['path_length_sum']
    print(sdf.to_csv())
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    args = parser.parse_args()
    main(args.input_folder)
