filename = "data/{path}.truth"
paths = glob_wildcards(filename).path
collections = ['safety', 'catfish', 'unitigs', 'modified_unitigs']
types = ['zebrafish', 'salmon', 'human', 'mouse']

rule all:
    input:
        expand("summary/comparisons/cfiltered_safety_fix/{p}.csv", p = paths)

rule run_compression_compare2fix:
    input:
        "result/cfiltered_safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/cfiltered_safety_fix/{p}.csv"
    shell:
        "python -m src.scripts.comparea -i {input[0]} -t {input[1]} >> summary/comparisons/cfiltered_safety_fix/{wildcards.p}.csv"

rule run_compression_compare2:
    input:
        "result/cfiltered_safety/{p}.res",
        "data/{p}.truth"
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

rule summaries2:
    input: 
        "summary/comparisons/{c}/"
    output:
        "summary/{c}/summary.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/{wildcards.c}/summary.csv"

rule summaries:
    input: 
        "summary/comparisons/{c}/rnaseq/{t}/"
    output:
        "summary/{c}/{t}summary.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/{wildcards.c}/{wildcards.t}summary.csv"
# sgr conversion is needed for catfish. 
# catfish doesn't take .graph files as an input
rule convert_to_sgr:
    input:
        "data/{p}.graph"
    output:
        "data/{p}.sgr"
    shell:
        "mv {input} {output}"

rule convert_to_gfa:
    input:
        "data/{p}.sgr"
    output:
        "data/{p}.sgr.gfa"
    shell:
        "python -m src.scripts.converter -i {input} >> data/{wildcards.p}.sgr.gfa"

rule run_catfish:
    input:
        "data/{p}.sgr"
    output:
        "result/catfish/{p}.res"
    shell:
        "./../catfish/bin/catfish -i {input} -o {output} -a greedy"

rule run_safety:
    input:
        "data/{p}.sgr.gfa"
    output:
        "result/safety/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} >> result/safety/{wildcards.p}.res"

rule run_safety_with_indices:
    input:
        "data/{p}.sgr.gfa"
    output:
        "result/safety_with_indices/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} -m 1 >> result/safety_with_indices/{wildcards.p}.res"

rule run_safety_with_naive_filtering:
    input:
        "data/{p}.sgr.gfa"
    output:
        "result/filtered_safety/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} -m 2 >> result/filtered_safety/{wildcards.p}.res"

rule run_unitigs:
    input:
        "data/{p}.sgr.gfa"
    output:
        "result/unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} >> result/unitigs/{wildcards.p}.res"

rule run_modified_unitigs:
    input:
        "data/{p}.sgr.gfa"
    output:
        "result/modified_unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} -m True >> result/modified_unitigs/{wildcards.p}.res"
        
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

rule modified_unitigs_truth_compare:
    input:
        "result/modified_unitigs/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/modified_unitigs/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/modified_unitigs/{wildcards.p}.csv"
rule filter_safety_compare:
    input:
        "result/filtered_safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/filtered_safety/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/filtered_safety/{wildcards.p}.csv"
