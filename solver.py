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
        self.num_points = len(points)
        self.dt = dt
        self.time = 0


        '''
        Elements of external_forces are tuples of the form: 
          1º element: Rope length fraction where the force is applied.
          2º element: Force to be applied.
        '''
        external_forces = (
            (.3, np.array([0, -1]) * G * 0.1,),
            (.6, np.array([1, 0]) * G * 0.1,),
        )
        external_forces = ()

        self.external_forces = []
        for p, f in external_forces:
            self.external_forces.append((int((self.num_points-1) * p), f))

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

            # damping_force += - (vec.dot((node.vel - s.points[side].get_vel(neighbor_side))) * node.damping) * vec
            # damping_force += - ((node.vel - s.points[side].get_vel(neighbor_side)) * node.damping)
        damping_force = -node.vel * node.damping

        return springs_force_total, damping_force, springs_force_max

    def point_acceleration(self, point: Point, update_tensions=False, id=None):
        springs_force, damping_force, spring_force_max = self.spring_forces(point)        
        if update_tensions:
            self.tensions[id] = spring_force_max

        weight = np.array([0, -1]) * G * point.mass

        total_force = springs_force + weight + damping_force

        for f_id, force in self.external_forces:
            if id == f_id:
                total_force += force
       
        acceleration = 1/point.mass* total_force

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
        self.middle_id = self.num_points//3

        ## Runge Kutta (RK4) ##
        pos_old = np.zeros((self.num_points, 2))
        vel_old = np.zeros((self.num_points, 2))
        for id, p in enumerate(self.points):
            pos_old[id] = p.pos
            vel_old[id] = p.vel

        k1_values = np.zeros((self.num_points, 4, 2))
        k2_values = np.zeros((self.num_points, 4, 2))
        
        k_id_to_update_tension = {0: True}
        k_id_to_q = {0: 1/2, 1: 1/2, 2: 1}
        
        def calc_ki(k_id, k1_values, k2_values):
            update_tension = k_id_to_update_tension.get(k_id, False)
            for id, p in enumerate(self.points):
                if p.fix:
                    self.point_acceleration(p, update_tensions=update_tension, id=id)
                    continue
                
                accel = self.point_acceleration(p, update_tensions=update_tension, id=id)
                k1 = p.vel
                k2 = accel

                k1_values[id][k_id] = k1
                k2_values[id][k_id] = k2
        
        def update_pos(k_id, k1_values, k2_values):
            q = k_id_to_q[k_id]
            for id, p in enumerate(self.points):
                if p.fix:
                    continue
                
                p.pos = pos_old[id] + q * self.dt * k1_values[id][k_id]
                p.vel = vel_old[id] + q * self.dt * k2_values[id][k_id]
        
        for k_id in (0, 1, 2, 3):
            calc_ki(k_id, k1_values, k2_values)
            
            if k_id != 3:
                update_pos(k_id, k1_values, k2_values)

        for id, p in enumerate(self.points):
            if p.fix:
                continue

            k11, k12, k13, k14 = k1_values[id]
            k21, k22, k23, k24 = k2_values[id]
            p.pos = pos_old[id] + self.dt/6 * (k11 + 2*(k12 + k13) + k14)
            p.vel = vel_old[id] + self.dt/6 * (k21 + 2*(k22 + k23) + k24)
        ##############


        ## Euler ##
        # ids: list[int] = []
        # new_pos = []
        # new_vel = []

        # for id, p in enumerate(self.points):
        #     accel = self.point_acceleration(p, update_tensions=True, id=id)
        #     if p.fix:
        #         continue

        #     next_pos = p.pos + p.vel * self.dt + self.dt**2/2 * accel
        #     next_vel = p.vel + accel * self.dt

        #     new_pos.append(next_pos)
        #     new_vel.append(next_vel)
        #     ids.append(id)
        
        # for id, pos, vel in zip(ids, new_pos, new_vel):
        #     self.points[id].pos = pos 
        #     self.points[id].vel = vel
        ##############

        self.time += self.dt

