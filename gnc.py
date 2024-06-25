from modsim import *
import numpy as np

settings = Params(
    turnover_time = 212,
    turnover_height = 2 * 1000,
    
    start_angle = np.deg2rad(-180),
    turnover_angle = np.deg2rad(-90 - 35),

    target_orbit = 2000 * 1000, # m
    final_angle = np.deg2rad(-90),
)

def get_set_angle(t, h):
    if h >= settings.target_orbit:
        return settings.final_angle
    if h >= settings.turnover_height:
    # if t >= settings.turnover_time:
        return settings.turnover_angle
    return settings.start_angle

def get_gnc(t, P, system):
    height_above_earth = vector_mag(P) - (0.5 * system.earth_diameter)

    # Get the angle the rocket is facing, relative to the rocket
    # Note: all incoming data is relative to earth
    set_angle = get_set_angle(t, height_above_earth)
    angle_to_earth = vector_angle(-1 * P)

    facing_angle = angle_to_earth - set_angle
    facing_cords = pol2cart(facing_angle, 1)
    facing_vector = vector_hat(Vector(facing_cords[0], facing_cords[1]))

    return Params(
        facing=facing_vector,
    )
    