import numpy as np
from modsim import *


def calc_gravity(P, system):
    height_above_earth = vector_mag(P) - (system.earth_diameter / 2)

    g = system.g0 * np.square(system.Re / (system.Re + height_above_earth))
    return g