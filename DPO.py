def remove_from_graph(G, L, K, mapping):
    for e in L.edges:
        if e not in K.edges:
            G.remove_edge(mapping[e[0]], mapping[e[1]])

    for n in L.nodes:
        if n not in K.nodes:
            G.remove_node(mapping[n])


def add_to_graph(G, K, R, mapping):
    i = G.nodes.length
    for n in R.nodes:
        if n not in K.nodes:
            G.add_node(i, {'label': n['label']})
            mapping[n] = i
            i += 1

    for e in R.edges:
        if e not in K.edges:
            G.add_edge(mapping[e[0]], mapping[e[0]], {'label': e['label']})


def double_pushout(G, L, K, R, mapping):
    remove_from_graph(G, L, K, mapping)
    add_to_graph(G, K, R, mapping)
