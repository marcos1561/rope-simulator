from rope_elements import Point, Side
import numpy as np
from constant import G, gravity_acel

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
        self.time = 0
        self.middle_id = len(points)//2

        self.tensions = np.zeros(len(self.points))
        self.acceleration = np.zeros(len(self.points))

    def spring_forces(self, node: Point, sides: list[int]=Side.sides()):
        '''
        Total force applied to the `node` by it's attached springs in the sides `sides`.
        '''
        springs_force_total = np.zeros(3)
        springs_force_max = 0
        damping_force = np.zeros(3)
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

    def wind_force(self, node: Point):
        if node.fix:
            return np.zeros(3)

        wind_force_density = 1
            
        wind_dir = np.array([0, 0, 1])
        p1 = node.springs[Side.left].get_pos(Side.left) - node.pos
        p2 = node.springs[Side.right].get_pos(Side.right) - node.pos

        ds1 = 1/2 * np.linalg.norm(p1 - (p1.dot(wind_dir))*wind_dir)
        ds2 = 1/2 * np.linalg.norm(p2 - (p2.dot(wind_dir))*wind_dir)
        
        wind_force = (ds1 + ds2) * wind_force_density * wind_dir
        return wind_force

    def point_acceleration(self, point: Point, update_tensions=False, update_accel=False, id=None):
        springs_force, damping_force, spring_force_max = self.spring_forces(point)        

        # wind_force = self.wind_force(point)
            
        # damping_force = -point.damping * np.linalg.norm(point.vel) * point.vel 
        weight = gravity_acel * point.mass

        acceleration = 1/point.mass*(springs_force + weight + damping_force)
        
        if update_accel:
            self.acceleration[id] = np.linalg.norm(acceleration)
        if update_tensions:
            self.tensions[id] = spring_force_max

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

            accel = self.point_acceleration(p, update_tensions=True, update_accel=True, id=id)
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
            self.time += self.dt
        
        for id, pos, vel in zip(ids, new_pos, new_vel):
            self.points[id].pos = pos 
            self.points[id].vel = vel
            # self.points[id].acel = acel

