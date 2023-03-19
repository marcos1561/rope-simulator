import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.artist import Artist
import numpy as np
from abc import ABC, abstractmethod

from solver import Solver
from rope import Rope
from config import ColorTensionConfig

class PlotMode:
    points = 0
    color_tension = 1

class RopeGraph(ABC):
    @abstractmethod
    def __init__(self, fig: Figure, ax: Axes, rope: Rope, additional_pars: dict, cfg) -> None:
        self.fig = fig
        self.ax = ax
        self.rope = rope
        self.cfg = cfg

        self.graph: Artist = None

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def adjust_limits(self, y: np.ndarray):
        ymin = self.ax.get_ylim()[0]
        rope_ymin = y.min()

        if rope_ymin * 1.1 < ymin:
            self.ax.set_ylim(bottom=rope_ymin * 1.1)

class Points(RopeGraph):
    def __init__(self, fig: Figure, ax: Axes, rope: Rope, additional_pars: dict, cfg) -> None:
        super().__init__(fig, ax, rope, additional_pars, cfg)
        self.graph: Line2D = None

    def init(self):
        x, y = self.rope.plot()
        self.graph, = self.ax.plot(x, y, "o-", color="Black")

    def update(self):
        x, y = self.rope.plot()
        self.graph.set_xdata(x)
        self.graph.set_ydata(y)

        self.adjust_limits(y)

class ColorTension(RopeGraph):
    def __init__(self, fig: Figure, ax: Axes, rope: Rope, additional_pars: dict, cfg) -> None:
        super().__init__(fig, ax, rope, additional_pars, cfg)

        self.solver: Solver = additional_pars["solver"]
        self.cfg: ColorTensionConfig
        self.graph: LineCollection = None

    def init(self):
        x, y = self.rope.plot()
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        norm = plt.Normalize(self.cfg.min, self.cfg.max)
        lc = LineCollection(segments, cmap='viridis', norm=norm)
        lc.set_array(self.solver.tensions)
        lc.set_linewidth(2)
        self.graph = self.ax.add_collection(lc)

        cbar = self.fig.colorbar(self.graph, ax=self.ax)
        cbar.ax.set_ylabel('Tensão (N)', rotation=270, labelpad=10)

    def update(self):
        x, y = self.rope.plot()
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        self.graph.set_segments(segments)
        self.graph.set_array(self.solver.tensions)
            
        self.adjust_limits(y)

rope_graph_manager: dict[int, RopeGraph] = {PlotMode.points: Points, PlotMode.color_tension: ColorTension}