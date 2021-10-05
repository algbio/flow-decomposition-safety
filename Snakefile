filename = "human/{path}.truth"
paths = glob_wildcards(filename).path
collections = ['safety', 'catfish', 'unitigs', 'modified_unitigs']

rule all:
    input:
        expand("summary/comparisons/catfish/{p}.metrics.json", p = paths),
        expand("summary/comparisons/safety/{p}.metrics.json", p = paths),
        expand("summary/comparisons/modified_unitigs/{p}.metrics.json", p = paths),
        expand("summary/comparisons/unitigs/{p}.metrics.json", p = paths)
        
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
# sg conversion is needed for catfish. 
rule convert_to_sg:
    input:
        "human/{p}.sg"
    output:
        "human/{p}.sgr"
    shell:
        "python -m src.scripts.converter -i {input} >> human/{wildcards.p}.sgr"

rule run_catfish:
    input:
        "human/{p}.sgr"
    output:
        "result/catfish/{p}.res"
    shell:
        "./../catfish/src/catfish -i {input} -o {output} -a greedy"

rule run_safety:
    input:
        "human/{p}.sg"
    output:
        "result/safety/{p}.res"
    shell:
        "python -m src.scripts.main -i {input} >> result/safety/{wildcards.p}.res"

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

rule run_unitigs:
    input:
        "human/{p}.sg"
    output:
        "result/unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} >> result/unitigs/{wildcards.p}.res"

rule run_modified_unitigs:
    input:
        "human/{p}.sg"
    output:
        "result/modified_unitigs/{p}.res"
    shell:
        "python -m src.scripts.unitigs -i {input} -m True >> result/modified_unitigs/{wildcards.p}.res"
        
rule cafish_truth_compare:
    input:
        "result/catfish/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.csv"
    shell:
        "python -m src.scripts.compare -c {input[0]} -t {input[1]} >> summary/comparisons/catfish/{wildcards.p}.csv"

rule cafish_truth_compare_seq:
    input:
        "result/catfish/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -c {input[0]} -t {input[1]} >> summary/comparisons/catfish/{wildcards.p}.metrics.json"


rule safety_truth_compare:
    input:
        "result/safety/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/safety/{wildcards.p}.csv"

rule safety_truth_compare_seq:
    input:
        "result/safety/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/safety/{wildcards.p}.metrics.json"


rule unitigs_truth_compare:
    input:
        "result/unitigs/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/unitigs/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/unitigs/{wildcards.p}.csv"

rule unitigs_truth_compare_seq:
    input:
        "result/unitigs/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/unitigs/{wildcards.p}.metrics.json"


rule modified_unitigs_truth_compare_seq:
    input:
        "result/modified_unitigs/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/modified_unitigs/{p}.metrics.json"
    shell:
        "python -m src.scripts.compare_seq -i {input[0]} -t {input[1]} >> summary/comparisons/modified_unitigs/{wildcards.p}.metrics.json"
rule filter_safety_compare:
    input:
        "result/filtered_safety/{p}.res",
        "human/{p}.truth"
    output:
        "summary/comparisons/filtered_safety/{p}.csv"
    shell:
        "python -m src.scripts.compare -i {input[0]} -t {input[1]} >> summary/comparisons/filtered_safety/{wildcards.p}.csv"
