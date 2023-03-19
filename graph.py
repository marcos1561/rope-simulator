import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.artist import Artist
import numpy as np
from abc import ABC, abstractmethod

from solver import Solver
from rope import Rope, Side
from config import ColorTensionConfig, ElasticRopeConfig, RopeConfig
import analitycal
from constant import G

class PlotMode:
    points = 0
    color_tension = 1

class RopeGraph(ABC):
    '''
    Rope graph manager. It is responsible for initialize and update the rope graph.
    '''

    @abstractmethod
    def __init__(self, fig: Figure, ax: Axes, rope: Rope, additional_pars: dict, cfg) -> None:
        self.fig = fig
        self.ax = ax
        self.rope = rope
        self.cfg = cfg

        self.graph: Artist = None

    @abstractmethod
    def init(self):
        '''
        Initial plot.
        '''
        pass

    @abstractmethod
    def update(self):
        '''
        Updates the plot.
        '''
        pass

    def adjust_limits(self, y: np.ndarray):
        '''
        Make sure all the rope is always on view.
        '''
        ymin = self.ax.get_ylim()[0]
        rope_ymin = y.min()

        if rope_ymin * 1.1 < ymin:
            self.ax.set_ylim(bottom=rope_ymin * 1.1)

class Points(RopeGraph):
    '''
    Plot the rope with black dots been rope nodes and dark lines been springs.
    '''

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
    '''
    Plot the rope with color representing the intensity of the tension.
    '''

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

        self.ax.set_title("Corda")

    def update(self):
        x, y = self.rope.plot()
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        self.graph.set_norm(plt.Normalize(self.solver.tensions.min(), self.solver.tensions.min()))
        self.graph.set_segments(segments)
        self.graph.set_array(self.solver.tensions)
            
        self.adjust_limits(y)


class AnalyticalRopesGraph:
    class RigidInfo:
        def __init__(self) -> None:
            self.max_tension: float = None

    class ElasticInfo:
        def __init__(self) -> None:
            self.tension: np.ndarray = None
    
    def __init__(self, ax: Axes, rope: Rope, solver: Solver, rope_cfg: RopeConfig) -> None:
        self.ax = ax

        self.rope = rope
        self.solver = solver
        self.rope_cfg = rope_cfg
    
        self.elastic_info = AnalyticalRopesGraph.ElasticInfo()
        self.rigid_info = AnalyticalRopesGraph.RigidInfo()

        self.elastic_graph: Line2D = None
        self.rigid_graph: Line2D = None

    def init(self):
        self.elastic_graph, = self.ax.plot([], [], color="red", label="Elástico")
        self.rigid_graph, = self.ax.plot([], [], "--", color="blue", label="Rígido")

    def update_elastic(self):
        elastic_tension = self.solver.spring_forces(self.rope.points[0], [Side.right])[0]
        self.elastic_info.tension = elastic_tension

        gap = self.rope.curve.length
        horizontal_tension = elastic_tension[0]
        cable_cfg = ElasticRopeConfig(self.rope_cfg.weight_density, self.rope_cfg.area, self.rope_cfg.elastic_constant)
        x, y = analitycal.elastic_rope(horizontal_tension, gap, cable_cfg)

        self.elastic_graph.set_xdata(x)
        self.elastic_graph.set_ydata(y)

    def update_rigid(self):
        flecha = self.rope.points[0].pos[1]
        length = 0
        for p in self.rope.points[1:]:
            length += np.linalg.norm(p.pos - p.springs[Side.left].get_pos(Side.left))
            if p.pos[1] < flecha:
                flecha = p.pos[1]
        flecha = abs(flecha)
        gap = self.rope.curve.length

        total_mass = self.rope.num_points * self.rope.point_mass
        w_o = total_mass / length * G

        # cabo = Cabo(flecha, gap, w_o)
        # try:
        #     cabo.calc_grandezas_todas()
        # except Exception as e:
        #     pars = {"w_o": w_o, "gap": gap, "flecha": flecha}
        #     print(f"Erro em gráfico rígido: pars={pars}")
        #     return

        # self.rigid_info.max_tension = cabo.T_max
        # x, y = cabo.catenaria_grafico()

        x, y, a = analitycal.catenary(x0=gap/2, y0=flecha)
        self.rigid_info.max_tension = a * w_o

        self.rigid_graph.set_xdata(x)
        self.rigid_graph.set_ydata(y)

    def update(self):
        self.update_rigid()
        self.update_elastic()

        print("Tensão:", np.linalg.norm(self.elastic_info.tension))
        print("Tensão horizontal:", abs(self.elastic_info.tension[0]))
        print()

        self.ax.legend()

class TensionGraph:
    def __init__(self, ax: Axes, solver: Solver) -> None:
        self.ax =ax
        self.solver = solver

        self.x = np.arange(len(self.solver.points))
    
        self.graph: Line2D = None

    def init(self):
        self.graph, = self.ax.plot(self.x, self.solver.tensions)

        self.ax.set_title("Tensão em cada nodo da corda")
        self.ax.set_ylabel("Tensão (N)")

    def update(self):
        self.graph.set_ydata(self.solver.tensions)
        
        ymin, ymax = self.ax.get_ylim()
        max_tension = self.solver.tensions.max()
        min_tension = self.solver.tensions.min()

        # delta = max_tension - min_tension
        # ymax_window = [max_tension + delta*0.2, max_tension + delta*0.4] 
        # ymin_window = [min_tension - delta*0.4, min_tension - delta*0.2] 

        # for limit, window_limit, ylim in (("top", ymax_window, ymax), ("bottom", ymin_window, ymin)):
        #     update_limit = False
        #     if ylim < window_limit[0]:
        #         new_ylim = window_limit[0]
        #         update_limit = True
        #     elif ylim > window_limit[1]:
        #         new_ylim = window_limit[1]
        #         update_limit = True

        #     if update_limit:
        #         self.ax.set_ylim(**{limit: new_ylim})

        if max_tension*1.1 > ymax:
            self.ax.set_ylim(top=max_tension*1.1)





rope_graph_manager_type: dict[int, RopeGraph] = {PlotMode.points: Points, PlotMode.color_tension: ColorTension}