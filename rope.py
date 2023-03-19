import numpy as np

from curves import Curve
from rope_elements import Point, Spring, Side
from config import ElementConfig, CreateConfig

class Rope:
    def __init__(self, curve: Curve, element_cfg: ElementConfig, create_cfg = CreateConfig()) -> None:
        self.curve = curve
        
        self.point_mass = element_cfg.mass
        self.spring_length = element_cfg.lenght
        self.k = element_cfg.k
        self.damping = element_cfg.damping
        
        self.create_cfg = create_cfg

        self.num_points = 0
        self.points = []

    def create(self):
        self.points = [Point(self.curve.curve(0), self.point_mass/2, fix=True)]
        s = self.spring_length

        while s < self.curve.length:
            point = Point(self.curve.curve(s), self.point_mass, damping=self.damping)
            
            self.points.append(point)

            spring = Spring(self.k, self.spring_length)
            self.points[-1].attach_spring(Side.left, spring)
            self.points[-2].attach_spring(Side.right, spring)

            s += self.spring_length* self.create_cfg.multiplier
        
        self.points[-1].mass *= 1/2
        self.points[-1].pos[0] = self.curve.length
        self.points[-1].fix = True

        self.num_points = len(self.points)
    
    def plot(self):
        x_list = np.zeros(self.num_points)
        y_list = np.zeros(self.num_points)
        for id in range(self.num_points):
            x_list[id] = self.points[id].pos[0]
            y_list[id] = self.points[id].pos[1]

            # xs = [self.points[id -1].pos[0], self.points[id].pos[0]]
            # ys = [self.points[id -1].pos[1], self.points[id].pos[1]]

            # x_list.extend(xs)
            # y_list.extend(ys)

            # plt.plot(xs, ys, color="black")
            # plt.plot(xs, ys, "o-", color="black")
            # plt.scatter(xs, ys)
        # plt.show()

        return x_list, y_list

