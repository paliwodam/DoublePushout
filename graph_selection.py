from matplotlib import pyplot as plt


class GraphSelection:
    def __init__(self, axis, callback=None):
        self.axis = axis
        self.range = 0.1
        self.data = []
        self.selectedCircles = {}
        self.callback = callback

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
                    self.callback()

    def draw_selected(self, axis, x, y, annotation):
        if (x, y, annotation) in self.selectedCircles:
            circle = self.selectedCircles[(x, y, annotation)]
            circle.set_visible(not circle.get_visible())
        else:
            circle = axis.scatter(
                x, y, marker="o", s=550, linewidths=2, facecolors="none", edgecolors="gold", zorder=-100
            )
            self.selectedCircles[(x, y, annotation)] = circle

        plt.show()

    def update(self, layout):
        self.data = []
        for i in layout:
            self.data.append((layout[i], i))

        self.selectedCircles = {}

    def get_selected(self):
        selected = []
        for x, y, i in self.selectedCircles:
            if self.selectedCircles[(x, y, i)].get_visible():
                selected.append(i)
        return selected
