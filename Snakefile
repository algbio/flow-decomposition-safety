import os, shutil

if os.path.isfile('data/catfish-output.txt'):
        os.remove('data/catfish-output.txt')

#shutil.copyfile('data/1.graph', 'data/1.sgr')

FILE = ""
if "file" in config:
    FILE = config['file']

PATH = f'data/{FILE}'

rule all:
    input:
        "data/comp.txt"

rule run_catfish:
    input:
        PATH
    output:
        "data/catfish-output.txt"
    shell:
        "./../catfish/bin/catfish -i {input} -o {output} -a greedy"


rule convert_to_gfa:
    input:
        PATH
    output:
        f"{PATH}.gfa"
    shell:
        "python scripts/parser.py --file {input}"


rule run_algorithm:
    input:
        f"{PATH}.gfa"
    output:
        "data/output.txt"
    shell:
        "python scripts/main.py --graph_file {input}"
        
rule compare:
    input:
        "data/catfish-output.txt",
        "data/output.txt",
        "data/1.truth"
    output:
        "data/comp.txt"
    shell:
        "python scripts/compare.py -co {input[0]} -so {input[1]} -gt {input[2]}"
