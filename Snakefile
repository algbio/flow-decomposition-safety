filename = "data/{path}.truth"
paths = glob_wildcards(filename).path

rule all:
    input:
        expand("data/{p}.sgr.gfa", p=paths)


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
        "python scripts/converter.py -i {input}"

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
        "python scripts/main.py -i {input} -o {output}"

rule test_safety_to_truth:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "result/test/{p}.tres"
    shell:
        "python scripts/test.py -safety {input[0]} -truth {input[1]} -o {output}"
        
rule cafish_truth_compare:
    input:
        "result/catfish/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/catfish/{p}.res"
    shell:
        "python scripts/compare.py -i {input[0]} -t {input[1]} -o {output}"

rule safety_truth_compare:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/comparisons/safety/{p}.res"
    shell:
        "python scripts/compare.py -i {input[0]} -t {input[1]} -o {output}"

rule safety_paths:
    input:
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "summary/paths/safety/{p}.res"
    shell:
        "python scripts/avg_length_path_length.py -i {input[0]} -t {input[1]} -o {output}"

rule cafish_paths:
    input:
        "result/catfish/{p}.res",
        "data/{p}.truth"
    output:
        "summary/paths/catfish/{p}.res"
    shell:
        "python scripts/avg_length_path_length.py -i {input[0]} -t {input[1]} -o {output}"
