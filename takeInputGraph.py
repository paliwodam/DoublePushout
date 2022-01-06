import networkx as nx


def takeInputGraph():
    input = 'graph.txt' # PLEASE CHANGE NAME OF THE INPUT FILE ﴾͡๏̯͡๏﴿

    G = nx.Graph()
    productions = []
    with open(input) as fp:
        #OPIS GRAFU

        n = int(fp.readline()) #amount of vertices
        for i in range(n):
            vert, label = fp.readline().split()
            vert = int(vert)
            label = str(label)
            G.add_node(vert, {'label': label})
        m = int(fp.readline())  # amount of edges

        for i in range(m):
            vert1, vert2, label = fp.readline().split()
            vert1 = int(vert1)
            vert2 = int(vert2)
            label = str(label)
            G.add_edge(vert1, vert2, {'label': label})


        #OPIS PRODUKCJI
        np = int(fp.readline()) #amount of productions
        for am in range(np):
            tab = []
            for j in range(3):
                P = nx.Graph()
                n = int(fp.readline())  # amount of vertices
                for i in range(n):
                    vert, label = fp.readline().split()
                    vert = int(vert)
                    label = str(label)
                    P.add_node(vert, {'label': label})
                m = int(fp.readline())  # amount of edges

                for i in range(m):
                    vert1, vert2, label = fp.readline().split()
                    vert1 = int(vert1)
                    vert2 = int(vert2)
                    label = str(label)
                    P.add_edge(vert1, vert2, {'label': label})
                tab.append(P)
            productions.append(tab)

    return G, productions
