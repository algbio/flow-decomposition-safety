rule run_catfish:
    input:
        config["catfishinput"]
    output:
        "outputtest.txt"
    shell:
        "./../catfish -i {input} -o {output} -a greedy"
''''
rule convert_to_gfa:
    input:
        "temp"
    shell:
        "python scripts/parser.py --file {input}"

rule run_algorithm:
    input:
        "data/dag_graph.gfa",
    shell:
        "python scripts/main.py --graph_file {input}

rule compare:
    input:
        "catsifh"
        "safety"
        "truth"
    shell:
        "python scripts/compare.py -co {input[0]} -so {input[1]} -gt {input[2]}"
'''''