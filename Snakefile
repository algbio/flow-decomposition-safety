import os

filename_seq = "data/seq/{path}.truth"
filename_nonseq = "data/nonseq/{path}.truth"
filename_all = "data/{path}.truth"
seq_paths = glob_wildcards(filename_seq).path
nonseq_paths = glob_wildcards(filename_nonseq).path
all_paths = glob_wildcards(filename_all).path
collections = ['SafeAndComp', 'Greedy', 'Unitigs', 'ExtUnitigs']
# collections = ['SafeAndComp', 'catfish', 'unitigs', 'modified_unitigs', 'SafeAndComp2', 'unitigs2', 'extUnitigs2']

#collections = ['SafeAndComp', 'catfish', 'unitigs']

rule all:
    input:
        "plots/seq/precision.png",
        "tables/seq/summary.txt",
        #"tables/nonseq/summary110.txt",
        "tables/seq/summary210.txt"
        #"plots/nonseq/precision.png",
        #"tables/nonseq/summary.txt"

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
        "result/ExtUnitigs/{p}.res"
    shell:
       	"./src/cpp-scripts/simp e < {input} | ./src/cpp-scripts/compress f > {output}"

rule run_unitigs2:
    input:
        "data/{p}.sgr"
    output:
        "result/Unitigs/{p}.res"
    shell:
       	"./src/cpp-scripts/simp u < {input} | ./src/cpp-scripts/compress f > {output}"

rule run_SafeComp2:
    input:
        "data/{p}.sgr"
    output:
        "result/SafeAndComp/{p}.res"
    shell:
       	"./src/cpp-scripts/simp < {input} | ./src/cpp-scripts/compress f > {output}"


rule run_catfish:
    input:
        "data/{p}.sgr"
    output:
        "result/Greedy/{p}.res"
    shell:
        "./../catfish/src/catfish -i {input} -o {output} -a greedy"

'''
rule run_SafeAndComp:
    input:
        "data/{p}.sg"
    output:
        "result/SafeAndComp/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} >> result/SafeAndComp/{wildcards.p}.res"

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
        "result/ExtUnitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/ExtUnitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/ExtUnitigs/{wildcards.p}.metrics.json"

rule unitigs_truth_compare_seq:
    input:
        "result/Unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/Unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/Unitigs/{wildcards.p}.metrics.json"

rule SafeComp_truth_compare_seq:
    input:
        "result/SafeAndComp/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/SafeAndComp/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/SafeAndComp/{wildcards.p}.metrics.json"


rule cafish_truth_compare:
    input:
        "result/Greedy/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/Greedy/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/Greedy/{wildcards.p}.metrics.json"

'''
rule SafeAndComp_truth_compare_seq:
    input:
        "result/SafeAndComp/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/SafeAndComp/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/SafeAndComp/{wildcards.p}.metrics.json"

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
        "python -m src.scripts.draw_plots -c summary/Greedy/summary_seq.csv -s summary/SafeAndComp/summary_seq.csv -u summary/Unitigs/summary_seq.csv -mu summary/ExtUnitigs/summary_seq.csv -p plots/seq/"

rule plot_nonseq:
    input: 
        sums = expand("summary/{c}/summary_nonseq.csv", c = collections)
    output:
        "plots/nonseq/precision.png"
    shell:
        "python -m src.scripts.draw_plots -c summary/Greedy/summary_nonseq.csv -s summary/SafeAndComp/summary_nonseq.csv -u summary/Unitigs/summary_nonseq.csv -mu summary/ExUnititgs/summary_nonseq.csv -p plots/nonseq/"
#aw_plots -c summary/catfish/summary_nonseq.csv -s summary/SafeAndComp/summary_nonseq.csv -u summary/unitigs/summary_nonseq.csv -p plots/nonseq/"

rule write_tables_seq:
    input:
        results = expand("summary/comparisons/{c}/seq/{p}.metrics.json", c=collections, p=seq_paths)
    output:
        "tables/seq/summary.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/SafeAndComp/seq -c summary/comparisons/Greedy/seq -u summary/comparisons/Unitigs/seq -mu summary/comparisons/ExtUnitigs/seq >> {output}"

rule write_tables_nonseq:
    input:
        results = expand("summary/comparisons/{c}/nonseq/{p}.metrics.json", c=collections, p=nonseq_paths)
    output:
        "tables/nonseq/summary.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/SafeAndComp/nonseq -c summary/comparisons/Greedy/nonseq -u summary/comparisons/Unitigs/nonseq -mu summary/comparisons/ExtUnitigs/nonseq  -b2 15 >> {output}"

rule write_tables_seq2:
    input:
        results = expand("summary/comparisons/{c}/seq/{p}.metrics.json", c=collections, p=seq_paths)
    output:
        "tables/seq/summary210.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/SafeAndComp/seq -c summary/comparisons/Greedy/seq -u summary/comparisons/Unitigs/seq -mu summary/comparisons/ExtUnitigs/seq -b2 10 >> {output}"

rule write_tables_nonseq2:
    input:
        results = expand("summary/comparisons/{c}/nonseq/{p}.metrics.json", c=collections, p=nonseq_paths)
    output:
        "tables/nonseq/summary110.txt"
    shell:
        "python -m src.scripts.gen_tables -s summary/comparisons/SafeAndComp/nonseq -c summary/comparisons/Greedy/nonseq -u summary/comparisons/Unitigs/nonseq -mu summary/comparisons/ExtUnitigs/nonseq -b2 10 >> {output}"
