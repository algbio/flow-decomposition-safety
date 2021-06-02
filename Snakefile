rule plot_graph:
    input:
        "data/dag_graph.gfa"
    script:
        "scripts/plot-graph.py"