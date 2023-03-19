import numpy as np
from numpy.linalg import norm
from abc import ABC, abstractmethod

class Curve(ABC):
    '''
    A parametrized curve with the parameter being it's length.
    '''

    def __init__(self) -> None:
        self.length: float # Total lenght of the curve   

    @abstractmethod
    def curve(self, s:float):
        '''
        Parametric function, where `s` is the parameters.

        This function must return the point (x(s), y(s)).
        '''
        pass

class Line(Curve):
    '''
    Straight line between two points
    '''

    def __init__(self, a: np.ndarray, b: np.ndarray) -> None:
        c = b - a
        self.c = c/norm(c)

        self.length = norm(c)

    def curve(self, s: float):
        return s * self.c 

class UCurve(Curve):
    '''
    Curve in the form of the letter u.
    '''

    def __init__(self, length:float, height: float) -> None:
        self.height = height
        self.ulength = length

        self.length = self.ulength + 2 * self.height

    def curve(self, s: float):
        if s < self.height:
            return np.array([0, -1]) * s
        elif s < (self.height + self.ulength):
            return np.array([0, -self.height]) + np.array([s-self.height, 0])
        else:
            return np.array([self.ulength, -self.height]) + np.array([0, s - self.height - self.ulength])




