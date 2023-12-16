from py2neo import Graph


def init_neo4j_graph(addr, auth):
    graph = Graph(addr, auth=auth)
    return graph

