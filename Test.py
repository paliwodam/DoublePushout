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
                    x, y, annotation = selected
                    print("Selected", annotation)
                    self.drawSelected(event.inaxes, x, y)

    def drawSelected(self, axis, x, y):
        if (x, y) in self.selectedCircles:
            circle = self.selectedCircles[(x, y)]
            circle.set_visible(not circle.get_visible())
        else:
            circle = axis.scatter(x+0.002, y+0.002, marker='o', s=200, linewidths=1,
                                  facecolors='none', edgecolors='red', zorder=-100)
            self.selectedCircles[(x, y)] = circle

        plt.show()


fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

G = nx.petersen_graph()
layout = nx.spring_layout(G, k=0.1, iterations=20)
nx.draw(G, layout, font_size=6, node_color='#A0CBE2', edge_color='#BB0000', width=0.1,
        node_size=2, with_labels=True, ax=ax1)

plt.connect('button_press_event', AnnoteFinder(layout, axis=ax1, range=0.1))

G = nx.petersen_graph()
layout = nx.spring_layout(G, k=0.1, iterations=20)
nx.draw(G, layout, font_size=6, node_color='#A0CBE2', edge_color='#BB0000', width=0.1,
        node_size=2, with_labels=True, ax=ax2)

plt.connect('button_press_event', AnnoteFinder(layout, axis=ax2, range=0.1))

plt.show()
