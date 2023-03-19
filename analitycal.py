import numpy as np
from scipy.optimize import fsolve
from scipy import integrate

from config import ElasticRopeConfig

def catenary(x0: float, y0: float, n=1000):
    '''
    Graph of the catenary which passes through the point (x0, y0) with x ranging between -xo and x0 
    in a coordinate system where the catenary minimum is at origin. The returned graph is in a 
    coordinate system where 0 < x < 2xo, y(0) = 0 and y(x0) = -y0, in other words, the graph was
    translated x0 units right and y0 units down.

    This function also return the `a` constant of the catenary.
    '''
    def func(x):
        return x * np.arccosh(y0/x + 1) - x0

    for init_a in np.logspace(-1, 4, 50, base=10):
        try:
            a = fsolve(func, init_a, maxfev=1000)[0]
            
            if func(a) > 1e-4:
                raise Exception()
            
            break
        except Exception:
            pass

    x = np.linspace(0, 2*x0, n)
    y = a *(np.cosh((x - x0)/a) - np.cosh(x0/a))

    return x, y, a

class EqSlope:
    '''
    Equation that the slope of an elastic rope must satisfied.
    '''
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

        self.x = 0

    def func(self, z):
        return z - np.sinh(self.x/self.a - self.b * z) 

def elastic_rope(horizontal_tension: float, gap_length:float, rope_cfg: ElasticRopeConfig, n=1000):
    '''
    Graph of an elastic rope with a given gap and horizontal tension, with x ranging between
    0 and `gap_length` in a coordinate system where y(0) = y(`gap_length`) = 0.

    The properties of the rope are in `rope_cfg`, for more info see documentation in `config.py`.
    '''
    a = horizontal_tension / rope_cfg.weight_density
    b= a * rope_cfg.weight_density / (rope_cfg.elastic_constant * rope_cfg.cross_section_area)

    eq = EqSlope(a, b)

    x = np.linspace(-gap_length/2, gap_length/2, n)
    derivate = np.zeros(x.size)

    init_x = np.sinh(x/a)/(b+1)

    debug = np.zeros(x.size)

    for id in range(x.size):
        eq.x = x[id]
        derivate[id] = fsolve(eq.func, init_x[id], maxfev=1000)[0]
        debug[id] = eq.func(derivate[id])

    rope_y = np.zeros(x.size)
    rope_y[1:] = integrate.cumulative_trapezoid(derivate, x)

    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig, ax1 = plt.subplots()

    # ax1.plot(x, np.concatenate([np.array([0]), rope_y]))
    # ax1.plot(x, catenaria(x, a), "--", color="red", label="Catenária")
    # ax1.plot(x, ys, color="red")
    # ax1.plot(x, np.sinh(x/a)/(b+1), "--")
    # ax1.plot(x, init_x, "--", color="red")
    # ax2.plot(x, debug)
    # plt.legend()
    # plt.show()

    return x+gap_length/2, rope_y

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    x, y = catenary(1, 1)

    plt.plot(x, y)
    plt.show()