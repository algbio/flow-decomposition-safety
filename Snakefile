import os

if os.path.isfile('data/catfish-output.txt'):
        os.remove('data/catfish-output.txt')

rule all:
    input:
        "data/catfish-output.txt",
        "data/1.sgr.gfa",
        "data/output.txt",
        "data/comp.txt"

rule run_catfish:
    input:
        "data/1.sgr"
    output:
        "data/catfish-output.txt"
    shell:
        "./../catfish/bin/catfish -i {input} -o {output} -a greedy"


rule convert_to_gfa:
    input:
        "data/1.sgr"
    output:
        "data/1.sgr.gfa"
    shell:
        "python scripts/parser.py --file {input}"


rule run_algorithm:
    input:
        "data/1.sgr.gfa"
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
