from numpy import deg2rad
from modsim import vector_hat, pol2cart
from turnover import calc_angle

def thrust_force(t, y, system):
    angle = calc_angle(y, system)
    max_thrust, burn_time = system.max_thrust, system.burn_time
    theta = deg2rad(angle)
    
    mag = max_thrust if t < burn_time else 0
    direction = vector_hat(pol2cart(theta, 1))
    f_thrust = mag * direction
    return f_thrust

if __name__ == "__main__":
    from modsim import Params
    print(thrust_force(5, 0, Params(
        max_thrust = 10,
        burn_time = 10,
        turnover_angle = 10,
        turnover_time = 10
    )))