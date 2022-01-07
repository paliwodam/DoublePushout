import networkx as nx
import matplotlib.pyplot as plt


class AnnoteFinder:
    def __init__(self, layout, axis, range):
        self.data = []
        for i in layout:
            self.data.append((layout[i], i))

        self.range = range
        self.axis = axis
        self.selectedCircles = {}

    def __call__(self, event):
        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
            if self.axis == event.inaxes:
                minimum_distance = float("inf")
                selected = None

                for (x, y), annotation in self.data:
                    dx, dy = abs(x - clickX), abs(y - clickY)
                    distance = dx * dx + dy * dy
                    if dx <= self.range and dy <= self.range and distance < minimum_distance:
                        minimum_distance = distance
                        selected = (x, y, annotation)

                if selected:
                    (x, y, annotation) = selected
                    self.drawSelected(event.inaxes, x, y, annotation)

    def drawSelected(self, axis, x, y, annotation):
        if (x, y, annotation) in self.selectedCircles:
            circle = self.selectedCircles[(x, y, annotation)]
            circle.set_visible(not circle.get_visible())
        else:
            circle = axis.scatter(x+0.002, y+0.002, marker='o', s=200, linewidths=1,
                                  facecolors='none', edgecolors='red', zorder=-100)
            self.selectedCircles[(x, y, annotation)] = circle

        plt.show()

    def getSelected(self):
        selected = []
        for x, y, i in self.selectedCircles:
            if self.selectedCircles[(x, y, i)].get_visible():
                selected.append(i)
        return selected


if __name__ == "__main__":
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    G = nx.petersen_graph()
    layout = nx.spring_layout(G, k=0.1, iterations=20)
    nx.draw(G, layout, font_size=6, width=0.1,
            node_color='#FFFFFF', node_size=5, ax=ax1)
    nx.draw_networkx_labels(G, layout, ax=ax1)
    nx.draw_networkx_edge_labels(G, layout, ax=ax1)

    plt.connect('button_press_event', AnnoteFinder(
        layout, axis=ax1, range=0.1))

    G = nx.petersen_graph()
    layout = nx.spring_layout(G, k=0.1, iterations=20)
    nx.draw(G, layout, font_size=6, node_color='#A0CBE2', edge_color='#BB0000', width=0.1,
            node_size=2, with_labels=True, ax=ax2)

    plt.connect('button_press_event', AnnoteFinder(
        layout, axis=ax2, range=0.1))

    plt.show()
