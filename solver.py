from rope_elements import Point, Side
import numpy as np
from constant import G

class Solver:
    def __init__(self, points: list[Point], dt: float) -> None:
        self.points = points
        self.dt = dt

        self.tensions = np.zeros(len(self.points))

    def spring_forces(self, rope_element: Point, sides=Side.sides()):
        springs_force_total = np.zeros(2)
        springs_force_max = 0
        damping_force = np.zeros(2)
        for side in sides:
            side: int
            s = rope_element.springs[side]

            if s == None:
                continue
            
            vec = s.get_pos(Side.right) - s.get_pos(Side.left)
            if side == Side.right:
                vec *= -1
            s_lenght = np.linalg.norm(vec)
            vec = vec / np.linalg.norm(vec)

            spring_force = - vec * s.k * (s_lenght - s.default_lenght)
            spring_force_norm = np.linalg.norm(spring_force)
            if spring_force_norm > springs_force_max:
                springs_force_max = spring_force_norm

            springs_force_total  += spring_force

            neighbor_side = Side.left
            if side == Side.left:
                neighbor_side = Side.right

            # damping_force += - (vec.dot((p.vel - s.points[side].get_vel(neighbor_side))) * p.damping) * vec
            damping_force += - ((rope_element.vel - s.points[side].get_vel(neighbor_side)) * rope_element.damping)

        return springs_force_total, damping_force, springs_force_max

    def update(self):
        ids: list[int] = []
        new_pos = []
        new_vel = []
        new_acel = []

        middle_id = len(self.points)//2

        for id, p in enumerate(self.points):
            if p.fix:
                springs_force, damping_force, spring_force_max = self.spring_forces(p)        
                self.tensions[id] = spring_force_max
                continue

            springs_force, damping_force, spring_force_max = self.spring_forces(p)
            self.tensions[id] = spring_force_max

            weight = np.array([0, -1]) * G * p.mass

            carga = np.zeros(2)
            # if id == middle_id:
            #     carga[1] =  - 100 * G

            current_acel = 1/p.mass*(springs_force + weight + damping_force + carga)

            next_pos = p.pos + p.vel * self.dt + self.dt**2/2 * current_acel
            next_vel = p.vel + current_acel * self.dt
            
            new_pos.append(next_pos)
            new_vel.append(next_vel)
            # new_acel.append(next_acel)
            ids.append(id)
        
        for id, pos, vel in zip(ids, new_pos, new_vel):
            self.points[id].pos = pos 
            self.points[id].vel = vel
            # self.points[id].acel = acel

