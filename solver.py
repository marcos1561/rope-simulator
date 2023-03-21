from rope_elements import Point, Side
import numpy as np
from constant import G

class Solver:
    '''
    Differential solver for newton second law.
    '''
    def __init__(self, points: list[Point], dt: float) -> None:
        '''
        Parameters:
            points:
                Rope nodes in order.
        '''
        self.points = points
        self.dt = dt

        self.tensions = np.zeros(len(self.points))

    def spring_forces(self, node: Point, sides: list[int]=Side.sides()):
        '''
        Total force applied to the `node` by it's attached springs in the sides `sides`.
        '''
        springs_force_total = np.zeros(2)
        springs_force_max = 0
        damping_force = np.zeros(2)
        for side in sides:
            side: int
            s = node.springs[side]

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
            damping_force += - ((node.vel - s.points[side].get_vel(neighbor_side)) * node.damping)

        return springs_force_total, damping_force, springs_force_max

    def point_acceleration(self, point: Point, update_tensions=False, id=None):
        springs_force, damping_force, spring_force_max = self.spring_forces(point)        
        if update_tensions:
            self.tensions[id] = spring_force_max

        weight = np.array([0, -1]) * G * point.mass
        acceleration = 1/point.mass*(springs_force + weight + damping_force)
        return acceleration

    def energy(self):
        energy = 0
        for p in self.points:
            energy += p.mass * np.linalg.norm(p.vel)**2 
            
            spring = p.springs[Side.left] 
            if spring != None:
                energy += spring.k * (spring.current_lenght - spring.default_lenght)**2            

            energy += 2 * p.mass * G * p.pos[1]

        return energy

    def update(self):
        '''
        Advance one time step.
        '''
        ids: list[int] = []
        new_pos = []
        new_vel = []

        middle_id = len(self.points)//2

        for id, p in enumerate(self.points):
            if p.fix:
                self.point_acceleration(p, update_tensions=True, id=id)
                continue
            
            ## Runge kutta ##
            pos0, vel0 = p.pos, p.vel

            accel = self.point_acceleration(p, update_tensions=True, id=id)
            k11 = p.vel
            k21 = accel

            p.pos = pos0 + self.dt/2 * k11
            p.vel = vel0 + self.dt/2 * k21
            accel = self.point_acceleration(p)

            k12 = p.vel
            k22 = accel
            
            p.pos = pos0 + self.dt/2 * k12
            p.vel = vel0 + self.dt/2 * k22
            accel = self.point_acceleration(p)

            k13 = p.vel
            k23 = accel
            
            p.pos = pos0 + self.dt * k13
            p.vel = vel0 + self.dt * k23
            accel = self.point_acceleration(p)

            k14 = p.vel
            k24 = accel
            
            next_pos = pos0 + self.dt/6 * (k11 + 2*(k12 + k13) + k14)
            next_vel = vel0 + self.dt/6 * (k21 + 2*(k22 + k23) + k24)
            p.pos, p.vel = pos0, vel0
            ###

            ## Euler ##
            # accel = self.point_acceleration(p, update_tensions=True, id=id)

            # next_pos = p.pos + p.vel * self.dt + self.dt**2/2 * accel
            # next_vel = p.vel + accel * self.dt
            ##############

            new_pos.append(next_pos)
            new_vel.append(next_vel)
            ids.append(id)
        
        for id, pos, vel in zip(ids, new_pos, new_vel):
            self.points[id].pos = pos 
            self.points[id].vel = vel
            # self.points[id].acel = acel

