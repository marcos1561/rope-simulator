import numpy as np

class Side:
    '''
    Class for naming the side index.
    '''
    left = 0
    right = 1

    @staticmethod
    def sides() -> tuple[int]:
        return Side.left, Side.right

class Spring:
    '''
    Massless Spring
    '''

    def __init__(self, k: float, default_lenght: float) -> None:
        '''
        Parameters:
            k: 
                spring constant.
            
            default_length:
                Length of the spring at equilibrium.
        '''

        self.k = k
        self.default_lenght = default_lenght

        self.points: list[Point] = [None, None] # Points which this spring is attached to.

    def get_pos(self, side: int):
        '''
        Position of the attached point in the side `side`.
        '''
        point_side = Side.right
        if side == Side.right:
            point_side = Side.left
        
        return self.points[side].get_pos(point_side)
    
    def get_vel(self, side: int):
        '''
        Velocity of the attached point in the side `side`.
        '''
        point_side = Side.right
        if side == Side.right:
            point_side = Side.left
        
        return self.points[side].get_vel(point_side)
    
    @property
    def current_lenght(self):
        return np.linalg.norm(self.pos(Side.left) - self.pos(Side.right))

class Point:
    '''
    Point mass
    '''

    def __init__(self, pos: np.ndarray, mass:float, vel: np.ndarray = np.zeros(2), damping: float = 0, fix=False) -> None:
        '''
        Parameters:
        -----------
        pos:
            Initial pos.
        
        vel:
            Initial velocity.
        
        mass:

        damping:
            The factor of the force that oppose to relative velocity with respect to it's neighbors mass points.

        fix:
            If `True`, this elements can't be moved by any force.
        '''

        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.acel = np.zeros([0, 0])
        self.damping= damping
    
        self.fix = fix

        self.springs: list[Spring] = [None, None] # Spring thar are attached to this element.

    def get_pos(self, side: int):
        return self.pos

    def get_vel(self, side: int):
        return self.vel

    def attach_spring(self, side: int, spring: Spring):
        '''
        Attach a spring in the side `side`.
        '''
        spring_side = Side.right
        if side == Side.right:
            spring_side = Side.left

        spring.points[spring_side] = self
        self.springs[side] = spring

if __name__ == "__main__":
    p = Point(np.array([1, 2]))
    s = Spring(1, 1)

    p.attach_spring(Side.left, s)
    
    print(s.right_pos)
    p.pos = np.array([4, 4])
    print(s.right_pos)
    