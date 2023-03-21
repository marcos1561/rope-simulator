
import numpy as np
from constant import G

class RopeConfig:
    '''
    Properties of the rope that will be simulated.
    '''

    def __init__(self, elastic_constant: float, diameter: float, mass_density: float = None, weight_density: float = None) -> None:
        '''
        All units are in IS.
        '''
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
    '''
    Properties of rope elements. There are two types os elements:
    
    -> Mass point

    -> Massless spring
    '''
    
    def __init__(self, k: float = None, length: float = None, mass: float = None, damping: float = 0) -> None:
        '''
        Mass point Properties:
        ----------------------
        mass:

        damping:
            The factor of the force that oppose to relative velocity of mass point with respect to it's neighbors.

        Massless Spring Properties:
        ---------------------------
        k: 
            spring constant.
        
        length:
            Length of the spring at equilibrium.
        '''

        self.k = k
        self.lenght = length
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
    '''
    Configuration for how the spring must be constructed.
    '''

    def __init__(self, multiplier: float = 1, last_fix=True) -> None:
        '''
        Parameters:
        -----------
            multiplier:
                When building the spring using a parametrized curve, after a node is placed, the curve parameter is increased by
                the spring length times `multiplier`.
                With a line curve, `multiplier > 1` causes the curve to start with some tension.
        '''

        self.multiplier = multiplier
        self.last_fix = last_fix

class ColorTensionConfig:
    '''
    Configuration for the rope plot, where colors in the rope indicate the intensity of
    the tension at that point.
    '''

    def __init__(self, max:float = None, min:float = None) -> None:
        self.max = max
        self.min = min

class ElasticRopeConfig:
    '''
    Properties for an elastic rope.
    '''

    def __init__(self, weight_density: float, cross_section_area: float, elastic_constant) -> None:
        self.weight_density= weight_density
        self.cross_section_area = cross_section_area
        self.elastic_constant = elastic_constant

class RigidRopeConfig:
    '''
    Parameters for a rigid rope (elastic constant tends to infinity).
    '''
    def __init__(self, flecha: float, weight_density: float, gap: float) -> None:
        self.flecha = flecha
        self.weight_density= weight_density
        self.gap = gap
