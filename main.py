from config import *
from simulation import Simulation, PlotMode
from curves import Line, UCurve

rope_cfg = RopeConfig(
    elastic_constant=1e2, 
    diameter=1, 
    weight_density=1)

element_cfg = ElementConfig(
    k=30,
    mass=1,
    length=0.4, 
    damping=0.5)

create_cfg = CreateConfig(
    multiplier=1,
    last_fix=True)

# curve = Line(np.array([0, 0, 0]), np.array([4, 0, 0]))
curve = UCurve(length=10, height=1)

rope_plot_mode = PlotMode.color_tension
show_tension = True
color_tension_cfg = ColorTensionConfig()

sim = Simulation(rope_cfg, element_cfg, create_cfg, curve, dt=0.01, rope_plot_mode=rope_plot_mode, 
    rope_graph_cfg=color_tension_cfg, show_tension=show_tension, match_spring_props=True,
    num_frame_steps=5)
print(element_cfg)

sim.run()
