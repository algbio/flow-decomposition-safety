import os

#if os.path.isdir('data'):
#    for root, dirs, files in os.walk('data'):
#        for d in dirs:
#            filename = "human/{path}.truth"
filename = "data/{path}.truth"
paths = glob_wildcards(filename).path
collections = ['safety', 'catfish', 'unitigs', 'modified_unitigs']

rule all:
    input:
        'plots/seq/precision.png'
'''
This is the pipeline for sequences
'''
# change data to correct form
rule convert_sg_to_sgr:
    input:
        "data/{p}.sg"
    output:
        "data/{p}.sgr"
    shell:
        "python -m src.scripts.converter -i {input} >> data/{wildcards.p}.sgr"

rule convert_graph_to_sgr:
    input:
        "data/{p}.graph"
    output:
        "data/{p}.sgr"
    shell:
        "mv {input} {output}"
        
# run the algorithms
rule run_catfish:
    input:
        "data/{p}.sgr"
    output:
        "result/catfish/{p}.res"
    shell:
        "./../catfish/src/catfish -i {input} -o {output} -a greedy"

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

# compare results from the algorithms without sequences
rule cafish_truth_compare:
    input:
        "result/catfish/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.csv"
    shell:
        "python -m src.scripts.compare -c {input[0]} -t {input[1]} >> summary/comparisons/catfish/{wildcards.p}.csv"

rule safety_truth_compare:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/safety/{wildcards.p}.csv"

rule unitigs_truth_compare:
    input:
        "result/unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/unitigs/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/unitigs/{wildcards.p}.csv"

# compare results from algorithm with sequences
rule cafish_truth_compare_seq:
    input:
        "result/catfish/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/catfish/{wildcards.p}.metrics.json"

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

# draw summaries without sequences
rule summaries:
    input: 
        "summary/comparisons/{c}/"
    output:
        "summary/{c}/summary.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/{wildcards.c}/summary.csv"

# draw summary with sequences
rule summaries_seq:
    input: 
        results = expand("summary/comparisons/{c}/{p}.metrics.json", c=collections, p=paths)
    output:
        "summary/{c}/summary_seq.csv"
    shell:
        "python -m src.scripts.summary_seq -i summary/comparisons/{wildcards.c}/ >> {output}"

# plot stuff
rule plot:
    input: 
        sums = expand("summary/{c}/summary_seq.csv", c =collections)
    output:
        "plots/seq/precision.png"
    shell:
        "python -m src.scripts.draw_plots -c summary/catfish/summary_seq.csv -s summary/safety/summary_seq.csv -u summary/unitigs/summary_seq.csv -p plots/seq/"

'''
end of sequence pipeline
'''

# other stuff
rule run_compression_compare2:
    input:
        "result/cfiltered_safety/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/cfiltered_safety/{p}.csv"
    shell:
        "python -m src.scripts.comparea -i {input[0]} -t {input[1]} >> summary/comparisons/cfiltered_safety/{wildcards.p}.csv"

rule run_compression:
    input:
        "result/cfiltered_safety/{p}.res",
        "result/safety_with_indices/{p}.res"
    output:
        "result/cfiltered_safety/{p}.res"
    shell:
        "./src/cpp-scripts/compress_acTrie < {input} > {output}"

rule run_safety_with_indices:
    input:
        "human/{p}.sgr.gfa"
    output:
        "result/safety_with_indices/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} -m 1 >> result/safety_with_indices/{wildcards.p}.res"

rule run_safety_with_naive_filtering:
    input:
        "human/{p}.sgr.gfa"
    output:
        "result/filtered_safety/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} -m 2 >> result/filtered_safety/{wildcards.p}.res"


rule filter_safety_compare:
    input:
        "result/filtered_safety/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/filtered_safety/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/filtered_safety/{wildcards.p}.csv"
