'''
Script to draw a summary of the dataset used in program.
TODO: Will be probably removed.
'''

#!/usr/bin/python3
import pandas as pd
import os


def main():

    write_file(
        ',graph number,dataset,type,numer of paths,path flows\n', f'output.csv')
    for root, dirs, files in os.walk('data'):
        for f in files:
            if f.split('.')[-1] == 'truth':
                filename = f'{root}/{f}'
                #filename = "data/rnaseq/human/1.truth"
                with open(filename, 'r') as fr:
                    row = {}
                    number_of_paths = 0
                    path_flows = []
                    for line in fr:
                        read = (line.rstrip()).split()
                        if read[0] == '#':
                            if row:
                                row['number of paths'] = number_of_paths
                                number_of_paths = 0
                                row['path flows'] = [path_flows]
                                path_flows = []
                                df = pd.DataFrame(row)
                                write_file(df.to_csv(
                                    header=False), "output.csv")
                                # I do not think this is a good idea, write_file opens the file every time it is called, but it could be opened
                                # once here and call write instead.
                                row = {}
                            row['graph_number'] = int(read[4])
                            row['dataset'] = filename.split('/')[-2]
                            row['type'] = filename.split('.')[-1]
                        else:
                            number_of_paths += 1
                            path_flows.append(int(read[0]))
                    if row:
                        row['number of paths'] = number_of_paths
                        number_of_paths = 0
                        row['path flows'] = [path_flows]
                        path_flows = []
                        write_file(pd.DataFrame(row).to_csv(
                            header=False), "output.csv")
                        # I do not think this is a good idea, write_file opens the file every time it is called, but it could be opened
                        # once here and call write instead.


def write_file(str, output):
    f = open(output, 'a')
    f.write(f'{str}')
if __name__ == '__main__':
    main()
