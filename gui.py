import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


'''
OPIS GRAFU:
<n> - liczba wierzchołków 
n linijek <i ETYKIETA> 
<m> - liczba krawędzi 
m linijek <i j ETYKIETY> 
<p> - liczba produkcji
p*3 razy <OPIS GRAFU>
'''

def takeInputGraph():
    input = 'graph.txt'  # PLEASE CHANGE NAME OF THE INPUT FILE ﴾͡๏̯͡๏﴿

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
            G.nodes[vert]['label'] = label
        m = int(fp.readline())  # amount of edges

        for i in range(m):
            vert1, vert2, label = fp.readline().split()
            vert1 = int(vert1)
            vert2 = int(vert2)
            label = str(label)
            G.add_edge(vert1, vert2)
            G[vert1][vert2]['label'] = label

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
                    P.nodes[vert]['label'] = label
                m = int(fp.readline())  # amount of edges

                for i in range(m):
                    vert1, vert2, label = fp.readline().split()
                    vert1 = int(vert1)
                    vert2 = int(vert2)
                    label = str(label)
                    P.add_edge(vert1, vert2)
                    P[vert1][vert2]['label'] = label
                tab.append(P)
            productions.append(tab)
    return G, productions


root = tk.Tk()

import networkx as nx
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


G,P = takeInputGraph()
fig = plt.figure(figsize = (10, 10))
ax = fig.add_subplot(2, 1, 1)
ax.set_title('select nodes to navigate there')
layout = nx.spring_layout(G, k = 0.1, iterations = 20)
nx.draw(G, layout, font_size = 10, node_color = '#A0CBE2', edge_color='#BB0000', width = 0.1,
        node_size = 2, with_labels=True)

plt.connect('button_press_event', AnnoteFinder(layout, range=0.1))

for i in range(len(P)):
    for j in range(3):
        ax1 = fig.add_subplot(2, 3, 3 + j + 1)
        layout1 = nx.spring_layout(G, k = 0.1, iterations = 20)
        nx.draw(P[i][j], layout1, font_size = 10, node_color='#A0CBE2', edge_color='#BB0000', width = 0.1,
        node_size = 2, with_labels=True)

line = FigureCanvasTkAgg(fig, root)
line.get_tk_widget().pack(side = tk.BOTTOM)

root.mainloop()


