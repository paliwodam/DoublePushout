from networkx import isomorphism
from networkx.classes.graph import Graph
from networkx.generators.small import petersen_graph

lb = "label"


def match_vertices(a, b):
    return a[lb] == b[lb]


def match_edges(a, b):
    return a[lb] == b[lb]


def get_isomorphism(L, K, G, selected):
    GM = isomorphism.GraphMatcher(G, L, match_vertices, match_edges)

    for iso in GM.subgraph_isomorphisms_iter():
        osi = {v: k for k, v in iso.items()}

        allSelected = all(map(lambda x: x in selected, iso.keys()))

        if allSelected:
            toBeRemoved = []
            for n in L.nodes:
                if n not in K.nodes:
                    toBeRemoved.append(osi[n])

            edgeConnectedOutside = False
            for r in toBeRemoved:
                for t in G[r]:
                    if t not in iso:
                        edgeConnectedOutside = True
                        break
                if edgeConnectedOutside:
                    break

            if not edgeConnectedOutside:
                return iso


if __name__ == "__main__":
    L = Graph()
    L.add_nodes_from([0, 1])
    L.nodes[0][lb] = 'A'
    L.nodes[1][lb] = 'B'
    L.add_edge(0, 1)
    for a, b in L.edges():
        L[a][b][lb] = 'E'

    K = Graph()
    K.add_nodes_from([1])
    K.nodes[1][lb] = 'B'

    G = petersen_graph()
    for n in G.nodes:
        G.nodes[n][lb] = 'A'
    G.nodes[5][lb] = 'B'

    for a, b in G.edges():
        G[a][b][lb] = 'E'

    G2 = Graph()
    G2.add_nodes_from([0, 1, 2])
    G2.nodes[0][lb] = 'A'
    G2.nodes[1][lb] = 'B'
    G2.nodes[2][lb] = 'C'
    G2.add_edge(0, 1)
    G2.add_edge(1, 2)
    for a, b in G2.edges():
        G2[a][b][lb] = 'E'

    print(get_isomorphism(L, K, G, [5, 8]))
    print(get_isomorphism(L, K, G2, [1, 2]))
    print(get_isomorphism(L, K, G2, [0, 1]))
