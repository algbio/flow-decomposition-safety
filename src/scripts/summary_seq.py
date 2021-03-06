'''
Draws a summary from datafolder given as a parameter.
'''
#!/usr/bin/python3
import argparse
import os
import pandas as pd

def main(input_folder, mode):
    '''
    Gets input folder as a parameter.
    Outputs a json-file containing summary of the data.
    '''
    
    df = read_file(input_folder)
    # reduce lists to single floats
    groups = df.groupby('k')
    sdf = groups.mean()
    sdf['number_of_graphs_per_k'] = groups.count().precision

    sdf['avg_path_length_seq'] = groups.sum()['seq_length_sum'] / groups.sum()['number_of_paths']
    sdf['avg_path_length_nodes'] = groups.sum()['node_sum'] / groups.sum()['number_of_paths']
    
    
    print(sdf.to_csv())

        

    #df = pd.concat(l)
        #for file in files:
        #    filename = f'{root}/{file}'
        #    print(filename)
    #filename = 'summary/comparisons/safety/16.metrics.json'
            #try:
            #    f = pd.read_json(filename)
            #except ValueError:
            #    continue
            #l.append(f)
    #df = pd.concat(l)
    '''
    # reduce lists to single floats
    column_strings = ['e_sizes_rel_vertex', 'e_size_rel_bases', 'max_cov_rel_vertex', 'max_cov_rel_bases']
    for c in column_strings:
        df[f'{c}_sum'] = [sum(x) for x in df[c]]
   
    groups = df.groupby('k')
    sdf = groups.mean()
    for c in column_strings:
        sdf[f'{c}_mean'] = sdf[f'{c}_sum']/sdf.index
    sdf['avg_path_length_seq'] = groups.sum()['seq_length_sum'] / groups.sum()['number_of_paths']
    sdf['avg_path_length_nodes'] = groups.sum()['node_sum'] / groups.sum()['number_of_paths']
    sdf ['avg_fscores_vertex'] = groups.mean()['fscore_vertex']
    sdf ['avg_fscores_vertex_weighted'] = groups.mean()['fscore_vertex_weighted']
    sdf['avg_fscores_bases'] = groups.mean()['fscore_bases']
    sdf['avg_fscores_bases_weighted'] = groups.mean()['fscore_bases_weighted']
    if sdf.index[0] == 0:
        print(sdf[1:].to_csv())
    else:
        print(sdf.to_csv())
    '''
def read_file(input_folder):
    l = []
    for root, dirs, files in os.walk(input_folder):
        # = root.split('/')[-1]
        if not dirs:
            for fi in files:
                filename= f'{root}/{fi}'
                try:
                    df = pd.read_json(filename)
                except ValueError:
                    continue
                l.append(df)
        else:
            for d in dirs:
                for r, d2, f in os.walk(f'{root}{d}'):
                    for fi in f:
                        filename= f'{r}/{fi}'
                        try:
                            df = pd.read_json(filename)
                        except ValueError:
                            continue
                        l.append(df)
    df = pd.concat(l)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_folder")
    parser.add_argument("-m", "--mode")
    args = parser.parse_args()
    main(args.input_folder, args.mode)
