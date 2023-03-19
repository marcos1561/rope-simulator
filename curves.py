import numpy as np
from numpy.linalg import norm
from abc import ABC, abstractmethod

class Curve(ABC):
    def __init__(self) -> None:
        self.length: float  

    @abstractmethod
    def curve(self, s:float):
        pass

class Line(Curve):
    def __init__(self, a: np.ndarray, b: np.ndarray) -> None:
        c = b - a
        self.c = c/norm(c)

        self.length = norm(c)

    def curve(self, s: float):
        return s * self.c 

class UCurve(Curve):
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




