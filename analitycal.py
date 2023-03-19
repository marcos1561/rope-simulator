import numpy as np
from scipy.optimize import fsolve
from scipy import integrate

from config import ElasticCableConfig

def catenaria(x, a):
    return a *(np.cosh(x/a) - np.cosh(x[0]/a))

class EqSlope:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

        self.x = 0

    def func(self, z):
        return z - np.sinh(self.x/self.a - self.b * z) 

def elastic_cable(n: int, gap_lenght:float, cfg: ElasticCableConfig):
    a = cfg.horizontal_tension / cfg.weight_density
    b= a * cfg.weight_density / (cfg.elastic_constant * cfg.cross_section_area)

    eq = EqSlope(a, b)

    x = np.linspace(-gap_lenght/2, gap_lenght/2, n)
    derivate = np.zeros(x.size)

    init_x = np.sinh(x/a)/(b+1)

    debug = np.zeros(x.size)

    for id in range(x.size):
        eq.x = x[id]
        derivate[id] = fsolve(eq.func, init_x[id], maxfev=1000)[0]
        debug[id] = eq.func(derivate[id])

    cable_y = np.zeros(x.size)
    cable_y[1:] = integrate.cumulative_trapezoid(derivate, x)

    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig, ax1 = plt.subplots()

    # ax1.plot(x, np.concatenate([np.array([0]), cable_y]))
    # ax1.plot(x, catenaria(x, a), "--", color="red", label="Catenária")
    # ax1.plot(x, ys, color="red")
    # ax1.plot(x, np.sinh(x/a)/(b+1), "--")
    # ax1.plot(x, init_x, "--", color="red")
    # ax2.plot(x, debug)
    # plt.legend()
    # plt.show()

    return x+gap_lenght/2, cable_y