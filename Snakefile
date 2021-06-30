filename = "data/{path}.truth"
paths = glob_wildcards(filename).path

rule all:
    input:
        expand("result/safety/{p}.res", p=paths)

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
        
rule compare:
    input:
        "result/catfish/{p}.res",
        "result/safety/{p}.res",
        "data/{p}.truth"
    output:
        "result/comparisons/{p}.res"
    shell:
        "python scripts/compare.py -co {input[0]} -so {input[1]} -gt {input[2]} -o {output}"
