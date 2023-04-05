from config import *
from simulation import Simulation, PlotMode
import curves

rope_cfg = RopeConfig(
    elastic_constant=1e2, 
    diameter=1, 
    weight_density=5)

element_cfg = ElementConfig(
    length=0.3, 
    damping=1)

create_cfg = CreateConfig(
    multiplier=1)

curve = curves.UCurve(height=1, length=4)

rope_plot_mode = PlotMode.color_tension
show_tension = True
color_tension_cfg = ColorTensionConfig()

sim = Simulation(rope_cfg, element_cfg, create_cfg, curve, dt=0.01, rope_plot_mode=rope_plot_mode, 
    rope_graph_cfg=color_tension_cfg, show_tension=show_tension)
print(element_cfg)

sim.run()
