from config import *
from simulation import Simulation, PlotMode
from curves import Line

rope_cfg = RopeConfig(
    elastic_constant=1e4, 
    diameter=0.01, 
    weight_density=0.7)

element_cfg = ElementConfig(
    k=100,
    mass=0.1,
    length=0.1, 
    damping=0.01)

create_cfg = CreateConfig(
    multiplier=1,
    last_fix=True,)

curve = Line(np.array([0, 0]), np.array([4, 0]))

rope_plot_mode = PlotMode.color_tension
show_tension = True
color_tension_cfg = ColorTensionConfig(
    min = 1,
    max = 2)

sim = Simulation(rope_cfg, element_cfg, create_cfg, curve, dt=0.01, rope_plot_mode=rope_plot_mode, 
    rope_graph_cfg=color_tension_cfg, show_tension=show_tension, match_spring_props=True, num_frame_steps=3)
print(element_cfg)

sim.run()
