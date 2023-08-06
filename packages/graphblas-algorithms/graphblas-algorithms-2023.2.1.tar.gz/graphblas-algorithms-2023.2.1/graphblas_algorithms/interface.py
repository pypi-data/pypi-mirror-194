from . import nxapi

#######
# NOTE: Remember to update README.md when adding or removing algorithms from Dispatcher
#######


class Dispatcher:
    # Boundary
    edge_boundary = nxapi.boundary.edge_boundary
    node_boundary = nxapi.boundary.node_boundary
    # Centrality
    degree_centrality = nxapi.centrality.degree_alg.degree_centrality
    eigenvector_centrality = nxapi.centrality.eigenvector.eigenvector_centrality
    in_degree_centrality = nxapi.centrality.degree_alg.in_degree_centrality
    katz_centrality = nxapi.centrality.katz.katz_centrality
    out_degree_centrality = nxapi.centrality.degree_alg.out_degree_centrality
    # Cluster
    average_clustering = nxapi.cluster.average_clustering
    clustering = nxapi.cluster.clustering
    generalized_degree = nxapi.cluster.generalized_degree
    square_clustering = nxapi.cluster.square_clustering
    transitivity = nxapi.cluster.transitivity
    triangles = nxapi.cluster.triangles
    # Community
    inter_community_edges = nxapi.community.quality.inter_community_edges
    intra_community_edges = nxapi.community.quality.intra_community_edges
    # Core
    k_truss = nxapi.core.k_truss
    # Cuts
    boundary_expansion = nxapi.cuts.boundary_expansion
    conductance = nxapi.cuts.conductance
    cut_size = nxapi.cuts.cut_size
    edge_expansion = nxapi.cuts.edge_expansion
    mixing_expansion = nxapi.cuts.mixing_expansion
    node_expansion = nxapi.cuts.node_expansion
    normalized_cut_size = nxapi.cuts.normalized_cut_size
    volume = nxapi.cuts.volume
    # DAG
    ancestors = nxapi.dag.ancestors
    descendants = nxapi.dag.descendants
    # Dominating
    is_dominating_set = nxapi.dominating.is_dominating_set
    # Isolate
    is_isolate = nxapi.isolate.is_isolate
    isolates = nxapi.isolate.isolates
    number_of_isolates = nxapi.isolate.number_of_isolates
    # Link Analysis
    hits = nxapi.link_analysis.hits_alg.hits
    pagerank = nxapi.link_analysis.pagerank_alg.pagerank
    # Reciprocity
    overall_reciprocity = nxapi.overall_reciprocity
    reciprocity = nxapi.reciprocity
    # Regular
    is_k_regular = nxapi.regular.is_k_regular
    is_regular = nxapi.regular.is_regular
    # Shortest Paths
    floyd_warshall = nxapi.shortest_paths.dense.floyd_warshall
    floyd_warshall_predecessor_and_distance = (
        nxapi.shortest_paths.dense.floyd_warshall_predecessor_and_distance
    )
    has_path = nxapi.shortest_paths.generic.has_path
    all_pairs_bellman_ford_path_length = (
        nxapi.shortest_paths.weighted.all_pairs_bellman_ford_path_length
    )
    single_source_bellman_ford_path_length = (
        nxapi.shortest_paths.weighted.single_source_bellman_ford_path_length
    )
    # Simple Paths
    is_simple_path = nxapi.simple_paths.is_simple_path
    # S Metric
    s_metric = nxapi.smetric.s_metric
    # Structural Holes
    mutual_weight = nxapi.structuralholes.mutual_weight
    # Tournament
    is_tournament = nxapi.tournament.is_tournament
    score_sequence = nxapi.tournament.score_sequence
    tournament_matrix = nxapi.tournament.tournament_matrix
    # Triads
    is_triad = nxapi.triads.is_triad

    @staticmethod
    def convert_from_nx(graph, weight=None, *, name=None):
        import networkx as nx

        from .classes import DiGraph, Graph, MultiDiGraph, MultiGraph

        if isinstance(graph, nx.MultiDiGraph):
            return MultiDiGraph.from_networkx(graph, weight=weight)
        if isinstance(graph, nx.MultiGraph):
            return MultiGraph.from_networkx(graph, weight=weight)
        if isinstance(graph, nx.DiGraph):
            return DiGraph.from_networkx(graph, weight=weight)
        if isinstance(graph, nx.Graph):
            return Graph.from_networkx(graph, weight=weight)
        raise TypeError(f"Unsupported type of graph: {type(graph)}")

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        from .classes import Graph

        if isinstance(obj, Graph):
            obj = obj.to_networkx()
        return obj

    @staticmethod
    def on_start_tests(items):
        try:
            import pytest
        except ImportError:  # pragma: no cover (import)
            return

        def key(testpath):
            filename, path = testpath.split(":")
            classname, testname = path.split(".")
            return (testname, frozenset({classname, filename}))

        # Reasons to skip tests
        multi_attributed = "unable to handle multi-attributed graphs"
        multidigraph = "unable to handle MultiDiGraph"
        multigraph = "unable to handle MultiGraph"

        # Which tests to skip
        skip = {
            key("test_mst.py:TestBoruvka.test_attributes"): multi_attributed,
            key("test_mst.py:TestBoruvka.test_weight_attribute"): multi_attributed,
            key("test_dense.py:TestFloyd.test_zero_weight"): multidigraph,
            key("test_weighted.py:TestBellmanFordAndGoldbergRadzik.test_multigraph"): multigraph,
        }
        for item in items:
            kset = set(item.keywords)
            for (test_name, keywords), reason in skip.items():
                if item.name == test_name and keywords.issubset(kset):
                    item.add_marker(pytest.mark.xfail(reason=reason))
