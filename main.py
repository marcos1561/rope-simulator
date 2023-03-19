from config import *
from simulation import Simulation, PlotMode
from curves import Line

rope_cfg = RopeConfig(
    elastic_constant=1e4, 
    diameter=0.01, 
    weight_density=0.7)

element_cfg = ElementConfig(
    lenght=0.05, 
    damping=0.1)

create_cfg = CreateConfig(
    multiplier=3)

curve = Line(np.array([0, 0]), np.array([4, 0]))

plot_mode = PlotMode.points
show_tension = True
color_tension_cfg = ColorTensionConfig(
    min = 1,
    max = 2)

sim = Simulation(rope_cfg, element_cfg, create_cfg, curve, dt=0.01, plot_mode=plot_mode, rope_graph_cfg=color_tension_cfg, show_tension=show_tension)
print(element_cfg)

sim.run()
