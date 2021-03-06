import networkx as nx
from networkx.exception import NetworkXException
from pylab import *
from graph_selection import GraphSelection
from input_graph import get_input_graph
from dpo import double_pushout
from isomorphism import get_isomorphism
import copy


class App:
    def __init__(self, input):
        G, self.productions = get_input_graph(input)

        self.G_stack = [G]

        self.curr_idx = 0

        self.fig = plt.figure(figsize=(10, 8))
        self.g_axis = self.fig.add_subplot(2, 1, 1)
        self.p_axis = [self.fig.add_subplot(2, 3, 4 + i) for i in range(3)]

        # Saved so they won't get garbage collected
        self.button_undo = add_button([0.10, 0.05, 0.1, 0.025], "Undo", lambda _: self.pop_graph_stack())
        self.button_prev = add_button([0.40, 0.05, 0.1, 0.025], "Previous", lambda _: self.prev())
        self.button_apply = add_button([0.5, 0.05, 0.1, 0.025], "Apply", lambda _: self.apply())
        self.button_next = add_button([0.60, 0.05, 0.1, 0.025], "Next", lambda _: self.next())

        self.graph_selection = GraphSelection(self.g_axis)
        plt.connect("button_press_event", self.graph_selection)

        self.draw(redraw_g=True)

    def next(self):
        self.curr_idx = (self.curr_idx + 1) % len(self.productions)
        self.draw()

    def prev(self):
        self.curr_idx = (self.curr_idx - 1 + len(self.productions)) % len(self.productions)
        self.draw()

    def get_G(self):
        return self.G_stack[-1]

    def get_L(self):
        return self.productions[self.curr_idx][0]

    def get_K(self):
        return self.productions[self.curr_idx][1]

    def get_R(self):
        return self.productions[self.curr_idx][2]

    def pop_graph_stack(self):
        if len(self.G_stack) > 1:
            self.G_stack.pop()
            self.draw(redraw_g=True)

    def apply(self):
        if len(self.get_L().nodes) != len(self.graph_selection.get_selected()):
            plt.xlabel("Nieprawidłowa ilość wierzchołków")
            plt.show()
            return

        mapping = get_isomorphism(self.get_L(), self.get_K(), self.get_G(), self.graph_selection.get_selected())

        if mapping is not None:
            new_G = copy.deepcopy(self.get_G())
            double_pushout(new_G, self.get_L(), self.get_K(), self.get_R(), mapping)
            self.G_stack.append(new_G)
            self.draw(redraw_g=True)
        else:
            plt.xlabel("Nie można dokonać transformacji")
            plt.show()

    def draw(self, redraw_g=False):
        if redraw_g:
            plt.xlabel(" ")
            self.g_axis.clear()
            g_layout = nx.spring_layout(self.get_G(), k=0.1, iterations=20, seed=123)
            self.graph_selection.update(g_layout)
            draw_graph(self.get_G(), g_layout, self.g_axis)

        for j in range(3):
            self.p_axis[j].clear()

            # Try to layout planarly, if can't do spring layout
            try:
                layout = nx.planar_layout(self.productions[self.curr_idx][j])
            except NetworkXException:
                layout = nx.spring_layout(self.productions[self.curr_idx][j], k=0.1, iterations=20, seed=123)

            draw_graph(self.productions[self.curr_idx][j], layout, self.p_axis[j])

        plt.show()


def draw_graph(g, layout, axis):
    vert_labels = {}
    for v in g.nodes:
        vert_labels[v] = g.nodes[v]["label"]

    edge_labels = {}
    for e in g.edges:
        edge_labels[e] = g[e[0]][e[1]]["label"]

    nx.draw(
        g,
        layout,
        font_size=8,
        width=0.1,
        node_color="lightsalmon",
        alpha=0.9,
        node_size=300,
        ax=axis,
    )
    nx.draw_networkx_labels(g, layout, font_size=10, labels=vert_labels, ax=axis)
    nx.draw_networkx_edge_labels(g, layout, edge_labels=edge_labels, ax=axis, font_size=8)


def add_button(position, label, callback):
    axis = plt.axes(position)
    button = Button(axis, label, color="bisque", hovercolor="tomato")
    button.label.set_fontsize(11)
    button.on_clicked(callback)
    return button

def main():
    # args = sys.argv[1]
    # app = App(args)
    app = App("ex1.txt")
    app.draw()

if __name__ == "__main__":
    main()