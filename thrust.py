from numpy import deg2rad
from modsim import vector_hat, pol2cart, Vector
import numpy as np

def thrust_force(t, gnc, settings):
    mag = settings.max_thrust if t < settings.burn_time else 0

    facing_cords = pol2cart(gnc.facing, 1)
    facing_vector = Vector(facing_cords[0], facing_cords[1])
    trust_direction = vector_hat(facing_vector)
    
    f_thrust = mag * trust_direction
    return f_thrust

if __name__ == "__main__":
    from modsim import Params
    print(thrust_force(5, 0, Params(
        max_thrust = 10,
        burn_time = 10,
        turnover_angle = 10,
        turnover_time = 10
    )))