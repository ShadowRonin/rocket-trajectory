import numpy as np
from modsim import *


def calc_gravity(P, system):
    height_above_earth = vector_mag(P) - (system.earth_diameter / 2)
    g = system.g0 * np.square(system.Re / (system.Re + height_above_earth))

    direction = -vector_hat(P)

    G = direction * g

    return G

if __name__ == "__main__":
    from modsim import Params
    print(calc_gravity(Vector(745891.9077555666, 6979487.591349284), Params(
        earth_diameter = 12756000,
        g0 = 9.8,
        Re = 6371000,
    )))

    print(calc_gravity(Vector(0, 6378000.0), Params(
        earth_diameter = 12756000,
        g0 = 9.8,
        Re = 6371000,
    )))