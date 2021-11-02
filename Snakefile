import os

filename_seq = "data/seq/{path}.truth"
filename_nonseq = "data/nonseq/{path}.truth"
filename_all = "data/{path}.truth"
seq_paths = glob_wildcards(filename_seq).path
nonseq_paths = glob_wildcards(filename_nonseq).path
all_paths = glob_wildcards(filename_all).path
collections = ['safety', 'catfish', 'unitigs', 'extended_unitigs']
# collections = ['safety', 'catfish', 'unitigs', 'modified_unitigs', 'safety2', 'unitigs2', 'extUnitigs2']

#collections = ['safety', 'catfish', 'unitigs']

rule all:
    input:
       "plots/seq/precision.png",
       "tables/seq/summary.txt",
       "plots/nonseq/precision.png",
       "tables/nonseq/summary.txt"

rule convert_sg_to_sgr:
    input:
        "data/seq/{p}.sg"
    output:
        "data/seq/{p}.sgr"
    shell:
        "python -m src.scripts.converter -i {input} >> data/seq/{wildcards.p}.sgr"


rule convert_graph_to_sgr:
    input:
        "data/nonseq/{p}.graph"
    output:
        "data/nonseq/{p}.sgr"
    shell:
        "mv {input} {output}"

rule convert_sgr_to_sg:
    input:
        "data/nonseq/{p}.sgr"
    output:
        "data/nonseq/{p}.sg"
    shell:
        "python -m src.scripts.converter -i {input} -m True >> data/nonseq/{wildcards.p}.sg"

rule run_extUnitigs2:
    input:
        "data/{p}.sgr"
    output:
        "result/extended_unitigs/{p}.res"
    shell:
       	"./src/cpp-scripts/simp e < {input} | ./src/cpp-scripts/compress f > {output}"

rule run_unitigs2:
    input:
        "data/{p}.sgr"
    output:
        "result/unitigs/{p}.res"
    shell:
       	"./src/cpp-scripts/simp u < {input} | ./src/cpp-scripts/compress f > {output}"

rule run_safety2:
    input:
        "data/{p}.sgr"
    output:
        "result/safety/{p}.res"
    shell:
       	"./src/cpp-scripts/simp < {input} | ./src/cpp-scripts/compress f > {output}"


rule run_catfish:
    input:
        "data/{p}.sgr"
    output:
        "result/catfish/{p}.res"
    shell:
        "./../catfish/src/catfish -i {input} -o {output} -a greedy"

'''
rule run_safety:
    input:
        "data/{p}.sg"
    output:
        "result/safety/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} >> result/safety/{wildcards.p}.res"

rule run_unitigs:
    input:
        "data/{p}.sg"
    output:
        "result/unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} >> result/unitigs/{wildcards.p}.res"


rule run_modified_unitigs:
    input:
        "data/{p}.sg"
    output:
        "result/modified_unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} -m True >> result/modified_unitigs/{wildcards.p}.res"
'''
# compare results from algorithm with sequences

rule extUnitigs_truth_compare_seq:
    input:
        "result/extended_unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/extended_unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/extended_unitigs/{wildcards.p}.metrics.json"

rule unitigs_truth_compare_seq:
    input:
        "result/unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/unitigs/{wildcards.p}.metrics.json"

rule safety_truth_compare_seq:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/safety/{wildcards.p}.metrics.json"


rule cafish_truth_compare:
    input:
        "result/catfish/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/catfish/{wildcards.p}.metrics.json"

'''
rule safety_truth_compare_seq:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/safety/{wildcards.p}.metrics.json"

rule unitigs_truth_compare_seq:
    input:
        "result/unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/unitigs/{wildcards.p}.metrics.json"

rule modified_unitigs_truth_compare_seq:
    input:
        "result/modified_unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/modified_unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/modified_unitigs/{wildcards.p}.metrics.json"
'''
# draw summary with sequences
rule summary_seq:
    input: 
        results = expand("summary/comparisons/{c}/seq/{p}.metrics.json", c=collections, p=seq_paths)
    output:
        "summary/{c}/summary_seq.csv"
    shell:
        "python -m src.scripts.summary_seq -i summary/comparisons/{wildcards.c}/seq/ >> {output}"

# draw summary without sequences
rule summary_nonseq:
    input: 
        results = expand("summary/comparisons/{c}/nonseq/{p}.metrics.json", c=collections, p=nonseq_paths)
    output:
        "summary/{c}/summary_nonseq.csv"
    shell:
        "python -m src.scripts.summary_seq -i summary/comparisons/{wildcards.c}/nonseq/ >> {output}"

# plot stuff
rule plot_seq:
    input: 
        sums = expand("summary/{c}/summary_seq.csv", c =collections)
    output:
        "plots/seq/precision.png"
    shell:
        "python -m src.scripts.draw_plots -c summary/catfish/summary_seq.csv -s summary/safety/summary_seq.csv -u summary/unitigs/summary_seq.csv -mu summary/extended_unitigs/summary_seq.csv -p plots/seq/"

rule plot_nonseq:
    input: 
        sums = expand("summary/{c}/summary_nonseq.csv", c = collections)
    output:
        "plots/nonseq/precision.png"
    shell:
        "python -m src.scripts.draw_plots -c summary/catfish/summary_nonseq.csv -s summary/safety/summary_nonseq.csv -u summary/unitigs/summary_nonseq.csv -mu summary/extended_unitigs/summary_nonseq.csv -p plots/nonseq/"
#aw_plots -c summary/catfish/summary_nonseq.csv -s summary/safety/summary_nonseq.csv -u summary/unitigs/summary_nonseq.csv -p plots/nonseq/"

rule write_tables_seq:
    input:
        results = expand("summary/comparisons/{c}/seq/{p}.metrics.json", c=collections, p=seq_paths)
    output:
        "tables/seq/summary.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/safety/seq -c summary/comparisons/catfish/seq -u summary/comparisons/unitigs/seq -mu summary/comparisons/extended_unitigs/seq >> {output}"

rule write_tables_nonseq:
    input:
        results = expand("summary/comparisons/{c}/nonseq/{p}.metrics.json", c=collections, p=nonseq_paths)
    output:
        "tables/nonseq/summary.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/safety/nonseq -c summary/comparisons/catfish/nonseq -u summary/comparisons/unitigs/nonseq -mu summary/comparisons/extended_unitigs/nonseq >> {output}"