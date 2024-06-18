import numpy as np

def calc_gravity(y, system):
    g = system.g0 * np.square(system.Re / (system.Re + y))
    return g