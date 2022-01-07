# import tkinter as tk
from takeInputGraph import takeInputGraph
from DPO import double_pushout
from matplotlib.axes import Axes
from isomorphism import get_isomorphism
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Manager:
    def __init__(self, G, productions):
        self.G = G
        self.productions = productions
        self.curr_idx = 0
        self.annoteFinder = None
        self.fig = plt.figure(figsize=(10, 10))
        self.layout = None
        self.ax = self.fig.add_subplot(2, 1, 1)
        self.ax1 = [self.fig.add_subplot(2, 3, 4),self.fig.add_subplot(2, 3, 5), self.fig.add_subplot(2, 3, 6)]

    def next(self):
        self.curr_idx = (self.curr_idx + 1) % len(self.productions)
        self.draw()

    def prev(self):
        self.curr_idx = (self.curr_idx - 1 + len(self.productions)) % len(self.productions)
        self.draw()

    def get_G(self):
        return self.G

    def get_L(self):
        return self.productions[self.curr_idx][0]

    def get_K(self):
        return self.productions[self.curr_idx][1]

    def get_R(self):
        return self.productions[self.curr_idx][2]

    def apply(self):
        mapping = get_isomorphism(self.get_L(), self.get_K(), self.get_G(), self.annoteFinder.get_selected())
        if mapping is not None:
            double_pushout(self.get_G(), self.get_L(), self.get_K(), self.get_R(), mapping)
            self.layout = None
            self.draw()

    def draw(self):
        if self.layout is None:
            self.ax.clear()
            # try:
            #     self.layout = nx.planar_layout(self.G)
            # except NetworkXException:
            #     self.layout = nx.spring_layout(self.G, k=0.1, iterations=20, seed=123)
            self.layout = nx.spring_layout(self.G, pos=self.layout, k=0.1, iterations=20, seed=123)
            verts, edges = label_helper(self.G)
            nx.draw(self.G, self.layout, width=0.1,
                    node_color='pink', alpha=0.9, node_size=200, ax= self.ax)
            nx.draw_networkx_labels(self.G, self.layout, labels=verts, font_size=6, ax=self.ax)
            nx.draw_networkx_edge_labels(self.G, self.layout, edge_labels=edges, ax=self.ax, font_size=6, font_color='red')

            self.annoteFinder = AnnoteFinder(self.layout, self.ax, range=0.1)
            plt.connect('button_press_event', self.annoteFinder)

        for j in range(3):
            self.ax1[j].clear()
            try:
                layout1 = nx.planar_layout(self.productions[self.curr_idx][j])
            except NetworkXException:
                layout1 = nx.spring_layout(self.productions[self.curr_idx][j], k=0.1, iterations=20, seed=123)
            # layout1 = nx.spring_layout(self.productions[self.curr_idx][j], k=0.1, iterations=20, seed=123)
            verts, edges = label_helper(self.productions[self.curr_idx][j])
            nx.draw(self.productions[self.curr_idx][j], layout1, font_size=6, width=0.1,
                    node_color='pink', alpha=0.9, node_size=200, ax=self.ax1[j])
            nx.draw_networkx_labels(self.productions[self.curr_idx][j], layout1, font_size=6, labels=verts, ax=self.ax1[j])
            nx.draw_networkx_edge_labels(self.productions[self.curr_idx][j], layout1, edge_labels=edges, ax=self.ax1[j],
                                         font_size=6, font_color='red')

        plt.show()

def label_helper(G):
    verts = {}
    for v in G.nodes:
        verts[v] = G.nodes[v]['label']

    edges = {}
    for e in G.edges:
        edges[e] = G[e[0]][e[1]]['label']
    return verts, edges
# root = tk.Tk()

import networkx as nx
from pylab import *



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
                    self.draw_selected(event.inaxes, x, y, annotation)

    def draw_selected(self, axis, x, y, annotation):
        if (x, y, annotation) in self.selectedCircles:
            circle = self.selectedCircles[(x, y, annotation)]
            circle.set_visible(not circle.get_visible())
        else:
            circle = axis.scatter(x+0.002, y+0.002, marker='o', s=200, linewidths=1,
                                  facecolors='none', edgecolors='red', zorder=-100)
            self.selectedCircles[(x, y, annotation)] = circle

        plt.show()

    def get_selected(self):
        selected = []
        for x, y, i in self.selectedCircles:
            if self.selectedCircles[(x, y, i)].get_visible():
                selected.append(i)
        return selected



G,P = takeInputGraph()
manager = Manager(G, P)

axprev = plt.axes([0.40, 0.05, 0.1, 0.025])
axnext = plt.axes([0.60, 0.05, 0.1, 0.025])
axapply = plt.axes([0.5, 0.05, 0.1, 0.025])

bnext = Button(axnext, 'Next')
bnext.on_clicked(lambda x: manager.next())

bprev = Button(axprev, 'Previous')
bprev.on_clicked(lambda x: manager.prev())

bapply = Button(axapply, 'Apply')
bapply.on_clicked(lambda x: manager.apply())

manager.draw()

plt.show()