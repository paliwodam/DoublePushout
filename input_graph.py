import networkx as nx


def get_input_graph(input):
    G = nx.Graph()
    productions = []
    with open(input) as fp:
        # OPIS GRAFU

        n = int(fp.readline())  # amount of vertices
        for i in range(n):
            vert, label = fp.readline().split()
            vert = int(vert)
            label = str(label)
            G.add_node(vert)
            G.nodes[vert]["label"] = label
        m = int(fp.readline())  # amount of edges

        for i in range(m):
            vert1, vert2, label = fp.readline().split()
            vert1 = int(vert1)
            vert2 = int(vert2)
            label = str(label)
            G.add_edge(vert1, vert2)
            G[vert1][vert2]["label"] = label

        fp.readline()
        # OPIS PRODUKCJI
        np = int(fp.readline())  # amount of productions
        for am in range(np):
            tab = []
            for j in range(3):
                P = nx.Graph()
                n = int(fp.readline())  # amount of vertices
                for i in range(n):
                    vert, label = fp.readline().split()
                    vert = int(vert)
                    label = str(label)
                    P.add_node(vert)
                    P.nodes[vert]["label"] = label
                m = int(fp.readline())  # amount of edges

                for i in range(m):
                    vert1, vert2, label = fp.readline().split()
                    vert1 = int(vert1)
                    vert2 = int(vert2)
                    label = str(label)
                    P.add_edge(vert1, vert2)
                    P[vert1][vert2]["label"] = label
                tab.append(P)
            productions.append(tab)
    return G, productions
