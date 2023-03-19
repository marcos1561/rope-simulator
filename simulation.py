import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation

# from PauloTCC.cabo import Cabo
import analitycal
import curves
from solver import Solver
from rope import Rope, Side
from config import *
from graph import PlotMode, rope_graph_manager, RopeGraph

class RigidInfo:
    def __init__(self) -> None:
        self.max_tension: float = None

class ElasticInfo:
    def __init__(self) -> None:
        self.tension: np.ndarray = None

class Simulation: 
    '''
    Simulated the rope with the given configurations and plot the simulation.
    '''

    def __init__(self, rope_cfg: RopeConfig, element_cfg: ElementConfig, create_cfg: CreateConfig, curve: curves.Curve, dt:float,
            rope_plot_mode=PlotMode.points, rope_graph_cfg=None, show_tension=False) -> None:
        self.cable_cfg = rope_cfg
        self.element_cfg = element_cfg
        self.curve = curve

        self.set_springs_parameters(rope_cfg, element_cfg)

        self.rope = Rope(curve=curve, element_cfg=element_cfg, create_cfg=create_cfg)
        self.rope.create()
        self.solver = Solver(self.rope.points, dt)

        self.plot_mode = rope_plot_mode
        self.rope_graph_cfg = rope_graph_cfg
        self.show_tension = show_tension

    @staticmethod
    def set_springs_parameters(cable_cfg: RopeConfig, element_cfg: ElementConfig):
        '''
        Set the rope spring element properties, such that the modeled rope macroscopic properties are
        the same as `self.rope_cfg`.
        '''            

        if element_cfg.lenght != None:
            element_cfg.k = cable_cfg.elastic_constant * cable_cfg.area / element_cfg.lenght
            element_cfg.mass = cable_cfg.mass_density * element_cfg.lenght
        elif element_cfg.k != None:
            element_cfg.lenght = cable_cfg.elastic_constant * cable_cfg.area / element_cfg.k
            element_cfg.mass = cable_cfg.mass_density * element_cfg.lenght
        elif element_cfg.mass != None:
            element_cfg.lenght = element_cfg.mass / cable_cfg.mass_density
            element_cfg.k = cable_cfg.elastic_constant * cable_cfg.area / element_cfg.lenght

    def run(self):
        '''
        Run the simulation while plotting it.
        '''
        self.rigid_info = RigidInfo()
        self.elastic_info = ElasticInfo()

        # Create and set figure and axes ###
        if self.show_tension:
            fig, (ax_rope, ax_tension) = plt.subplots(1, 2, figsize=(14, 6))
            ax_tension.set_ylim(0, 0.01)
        else:
            fig, ax_rope = plt.subplots(figsize=(13, 5))
        ax_rope.set_ylim(-1, 0.5)
        ####

        # Creates rope graph manager ###
        additional_pars = None
        if self.plot_mode == PlotMode.color_tension:
            additional_pars = {"solver": self.solver}
        rope_graph: RopeGraph = rope_graph_manager[self.plot_mode](fig, ax_rope, self.rope, additional_pars, self.rope_graph_cfg)
        ###

        rope_graph.init()
        elastic_graph, = ax_rope.plot([], [], color="red", label="Elástico")
        rigid_graph, = ax_rope.plot([], [], "--", color="blue", label="Rígido")
        
        if self.show_tension:
            tension_x = np.arange(len(self.rope.points))
            tension_graph, = ax_tension.plot(tension_x, self.solver.tensions)
            ax_tension.set_ylabel("Tensão (N)")

        # Room for button
        fig.subplots_adjust(left=0.15)

        # damp_vec =  ax.quiver([pos[0], pos[0]], [pos[1], pos[1]], [0.1, -0.1], [2, 2], color=["red", "green"], angles='xy', scale_units='xy', scale=1)
        
        def update(frame):
            self.solver.update()

            rope_graph.update()

            if self.show_tension:
                # tension_graph.set_offsets(np.array([tension_x, self.solver.tensions]).transpose())
                tension_graph.set_ydata(self.solver.tensions)
                ymax = ax_tension.get_ylim()[1]
                max_tension = self.solver.tensions.max()
                if max_tension*1.1 > ymax:
                    ax_tension.set_ylim(top=max_tension*1.1)

            # print(np.linalg.norm(damping_force))
            # damp_vec.set_offsets([p.pos[0], p.pos[1]])
            # damp_vec.set_UVC([damping_force[0]], [damping_force[1]])
            # update_buttom(None)

            fig.canvas.draw_idle()

        

        ax_y1 = ax_rope.get_position().y1
        button_height = 0.04
        offset = 0.01
        button_ax = fig.add_axes([offset,ax_y1-button_height, 0.1, button_height])
        button = Button(button_ax, 'Cabos', hovercolor='0.975')

        def draw_analytical_cables(event):
            x, y = self.elastic_cable_graph()
            elastic_graph.set_xdata(x)
            elastic_graph.set_ydata(y)

            rigid_x, rigid_y = self.rigid_cable_graph()
            rigid_graph.set_xdata(rigid_x)
            rigid_graph.set_ydata(rigid_y)

            print("Tension")
            print("Elastic horizontal:", self.elastic_info.tension[0])
            print("Elastic :", np.linalg.norm(self.elastic_info.tension))
            print("Rigid   :", self.rigid_info.max_tension)
            print()

            ax_rope.legend()
            fig.canvas.draw_idle()
        button.on_clicked(draw_analytical_cables)

        ani = animation.FuncAnimation(fig, update, interval=self.solver.dt*1000/5)
        
        plt.show()

    def elastic_cable_graph(self):
        elastic_tension = self.solver.spring_forces(self.rope.points[0], [Side.right])[0]
        self.elastic_info.tension = elastic_tension

        gap = self.curve.length
        horizontal_tension = elastic_tension[0]
        cable_cfg = ElasticCableConfig(self.cable_cfg.weight_density, self.cable_cfg.area, self.cable_cfg.elastic_constant)
        x, y = analitycal.elastic_cable(horizontal_tension, gap, cable_cfg)

        return x, y

    def rigid_cable_graph(self):
        flecha = self.rope.points[0].pos[1]
        # length = 0
        for p in self.rope.points[1:]:
            # length += np.linalg.norm(p.pos - p.springs[Side.left].get_pos(Side.left))
            if p.pos[1] < flecha:
                flecha = p.pos[1]
        flecha = abs(flecha)
        gap = self.curve.length

        # total_mass = len(self.rope.points) * self.rope.point_mass
        # w_o = total_mass / length * G

        # cabo = Cabo(flecha, gap, w_o)

        # try:
        #     cabo.calc_grandezas_todas()
        # except Exception as e:
        #     pars = {"w_o": w_o, "gap": gap, "flecha": flecha}
        #     print(f"Erro em gráfico rígido: pars={pars}")
        #     return

        # self.rigid_info.max_tension = cabo.T_max
        # x, y = cabo.catenaria_grafico()

        x, y = analitycal.catenary(x0=gap/2, y0=flecha)
        return x, y

