import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.animation as animation

# from PauloTCC.cabo import Cabo
import curves
from solver import Solver
from rope import Rope
from config import *
from graph import PlotMode, rope_graph_manager_type, RopeGraph, AnalyticalRopesGraph, TensionGraph, Info
from timer import TimeIt


class Simulation: 
    '''
    Simulated the rope with the given configurations and plot the simulation.
    '''
    def __init__(self, rope_cfg: RopeConfig, element_cfg: ElementConfig, create_cfg: CreateConfig, curve: curves.Curve, 
        dt:float, rope_plot_mode=PlotMode.points, rope_graph_cfg=None, show_tension=False, match_spring_props=True, fps=120, num_frame_steps=1) -> None:
        self.rope_cfg = rope_cfg
        self.element_cfg = element_cfg
        self.curve = curve

        if match_spring_props:
            self.match_springs_properties(rope_cfg, element_cfg)

        self.rope = Rope(curve=curve, element_cfg=element_cfg, create_cfg=create_cfg)
        self.rope.create()
        self.solver = Solver(self.rope.points, dt)

        self.plot_mode = rope_plot_mode
        self.rope_graph_cfg = rope_graph_cfg
        self.show_tension = show_tension

        self.fps = fps
        self.num_frame_steps = num_frame_steps

        self.time_it = TimeIt(num_samples=200)

    @staticmethod
    def match_springs_properties(cable_cfg: RopeConfig, element_cfg: ElementConfig):
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
        ## Create and set figure and axes ###
        if self.show_tension:
            fig, (ax_rope, ax_tension) = plt.subplots(1, 2, figsize=(14, 6))
            ax_tension.set_ylim(0, 0.01)
        else:
            fig, ax_rope = plt.subplots(figsize=(13, 5))
        ax_rope.set_ylim(-1, 0.5)

        # Analytical ropes
        fig.subplots_adjust(left=0.15)
        ax_y1 = ax_rope.get_position().y1
        button_height = 0.04
        offset = 0.01
        button_ax = fig.add_axes([offset,ax_y1-button_height, 0.1, button_height])
        button = Button(button_ax, 'Cabos', hovercolor='0.975')

        def draw_analytical_ropes(event):
            analytical_ropes_graph.update()
            fig.canvas.draw_idle()
        button.on_clicked(draw_analytical_ropes)
        
        # Info
        info_ax = fig.add_axes([0.01, 0.9, 0.1, 0.04])
        ####

        # Creates graphs managers ###
        additional_pars = None
        if self.plot_mode == PlotMode.color_tension:
            additional_pars = {"solver": self.solver}
        rope_graph: RopeGraph = rope_graph_manager_type[self.plot_mode](fig, ax_rope, self.rope, additional_pars, self.rope_graph_cfg)
        
        analytical_ropes_graph = AnalyticalRopesGraph(ax_rope, self.rope, self.solver, self.rope_cfg)
        
        tension_graph = TensionGraph(ax_tension, self.solver)

        info_widget = Info(info_ax, self.solver, self.time_it)
        ###

        info_widget.init()
        rope_graph.init()
        analytical_ropes_graph.init()
        if self.show_tension:
            tension_graph.init()

        # damp_vec =  ax.quiver([pos[0], pos[0]], [pos[1], pos[1]], [0.1, -0.1], [2, 2], color=["red", "green"], angles='xy', scale_units='xy', scale=1)
        def update(frame):
            i = 0
            while i < self.num_frame_steps:
                self.time_it.decorator(self.solver.update)
                i += 1
            
            info_widget.update()
            rope_graph.update()
            if self.show_tension:
                tension_graph.update()

            # print(np.linalg.norm(damping_force))
            # damp_vec.set_offsets([p.pos[0], p.pos[1]])
            # damp_vec.set_UVC([damping_force[0]], [damping_force[1]])
            # update_buttom(None)

            fig.canvas.draw_idle()

        ani = animation.FuncAnimation(fig, update, interval=1/(self.fps)*1000)
        
        plt.show()
