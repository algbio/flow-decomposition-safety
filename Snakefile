rule run_algorithm:
    input:
        "data/dag_graph.gfa",
    shell:
        "python scripts/main.py --graph_file {input} -s 0 -t 7"