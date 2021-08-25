filename = "data/{path}.truth"
paths = glob_wildcards(filename).path

rule all:
    input:
        "summary/safety_summary.csv"

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
        "python -m src.scripts.main -i {input} -m True >> result/safety_with_indices/{wildcards.p}.res"

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

rule summary_safety:
    input: 
        "summary/comparisons/safety/"
    output:
        "summary/safety.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/safety_summary.csv"

rule summary_catfish:
    input: 
        "summary/comparisons/catfish/"
    output:
        "summary/catfish.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/catfish_summary.csv"

rule summary_unitigs:
    input: 
        "summary/comparisons/unitigs/"
    output:
        "summary/unitigs.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/unitigs_summary.csv"

rule summary_modifies_unitigs:
    input: 
        "summary/comparisons/modified_unitigs/"
    output:
        "summary/modified_unitigs.csv"
    shell:
        "python -m src.scripts.summary -i {input} >> summary/modified_unitigs_summary.csv"