
import numpy as np
from constant import G

class RopeConfig:
    def __init__(self, elastic_constant: float, diameter: float, mass_density: float = None, weight_density: float = None) -> None:
        if weight_density == None and mass_density == None:
            raise TypeError("CableConfig.__init__() não pode ter ambos 'mass_density' e 'weight_density' não fornecidos.")

        self.__diameter: float = None
        self.__area: float = None
        self.__mass_density: float = None
        self.__weight_density: float = None

        self.elastic_constant = elastic_constant
        self.mass_density = mass_density
        self.weight_density = weight_density
        self.diameter = diameter

    @property
    def mass_density(self):
        return self.__mass_density

    @mass_density.setter
    def mass_density(self, value: float):
        if value == None:
            return

        self.__mass_density = value
        self.__weight_density = value * G
    
    @property
    def weight_density(self):
        return self.__weight_density

    @weight_density.setter
    def weight_density(self, value: float):
        if value == None:
            return
        
        self.__weight_density = value
        self.__mass_density = value / G

    @property
    def diameter(self):
        return self.__diameter
    
    @diameter.setter
    def diameter(self, value: float):
        self.__diameter = value
        self.__area = np.pi * (value/2)**2

    @property
    def area(self):
        return self.__area

class ElementConfig:
    def __init__(self, k: float = None, lenght: float = None, mass: float = None, damping: float = 0) -> None:
        self.k = k
        self.lenght = lenght
        self.mass = mass
        self.damping = damping
    
    def __str__(self) -> str:
        return (
            f"k       :{self.k:.3f}\n"
            f"length  :{self.lenght:.5f}\n"
            f"mass    :{self.mass:.5f}\n"
            f"damping :{self.damping:.3f}\n"
        )

class CreateConfig:
    def __init__(self, multiplier: float = 1) -> None:
        self.multiplier = multiplier

class ColorTensionConfig:
    def __init__(self, max:float = None, min:float = None) -> None:
        self.max = max
        self.min = min

class ElasticCableConfig:
    def __init__(self, horizontal_tension: float, weight_density: float, cross_section_area: float, elastic_constant) -> None:
        self.horizontal_tension = horizontal_tension
        self.weight_density= weight_density
        self.cross_section_area = cross_section_area
        self.elastic_constant = elastic_constant

class RigidCableConfig:
    def __init__(self, flecha: float, weight_density: float, gap: float) -> None:
        self.flecha = flecha
        self.weight_density= weight_density
        self.gap = gap
