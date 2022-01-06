import networkx as nx
import matplotlib.pyplot as plt
import graphistry
from pylab import *


class AnnoteFinder:
    def __init__(self, layout, range):
        self.data = []
        for i in layout:
            self.data.append((layout[i], i))

        self.range = range
        self.axis = plt.gca()
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
                    self.drawSelected(event.inaxes, x, y, annotation)

    def drawSelected(self, axis, x, y, annote):
        if (x, y) in self.selectedCircles:
            circle = self.selectedCircles[(x, y)]
            circle.set_visible(not circle.get_visible())
        else:
            circle = axis.scatter(x+0.002, y+0.002, marker='o', s=200, linewidths=1,
                                  facecolors='none', edgecolors='red', zorder=-100)
            self.selectedCircles[(x, y)] = circle

        self.axis.figure.canvas.draw()


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
ax.set_title('select nodes to navigate there')

G = nx.petersen_graph()
layout = nx.spring_layout(G, k=0.1, iterations=20)
nx.draw(G, layout, font_size=6, node_color='#A0CBE2', edge_color='#BB0000', width=0.1,
        node_size=2, with_labels=True)

plt.connect('button_press_event', AnnoteFinder(layout, range=0.1))

plt.show()


