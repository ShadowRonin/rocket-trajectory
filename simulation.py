
# import functions from modsim
from modsim import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

from drag import drag_force
from gnc import get_gnc
from numpy import pi, deg2rad
from vehicle import Vehicle
from gravity import calc_gravity

# Set up params, all metric
params = Params(
    x = 0,
    starting_speed = 0,

    g0 = 9.8,        # m/s**2
    Re = 6371000,

    t_end = 300000,     # s

    C_d = 1.82, # of a baseball

    earth_diameter = 12756000, # meters

    #booster AJ-60A from an Atlas V
    diameter = 	1.6,
)

def make_system(params):
    y = (params.earth_diameter / 2) + 10 # start slightly above the surface
    P = Vector(params.x, y)

    # convert angle to radians
    gnc = get_gnc(0, P, Vector(0, 0), params)
    
    # compute x and y components of velocity
    vx, vy = params.starting_speed * gnc.facing
    
    init = State(x=params.x, y=y, vx=vx, vy=vy)
    
    # compute the frontal area
    area = pi * (params.diameter/2)**2

    # The data we want to track
    telemetry = {
        't': [],
        'x': [],
        'y': []
    }
    # telemetry = {
    #     'x': pd.Series(),
    #     'y': pd.Series(),
    #     'ax': pd.Series(),
    #     'ay': pd.Series(),
    #     'gx': pd.Series(),
    #     'gy': pd.Series(),
    #     'trust_a': pd.Series(),
    #     'atx': pd.Series(),
    #     'aty': pd.Series(),
    #     'trust_f': pd.Series(),
    #     'ftx': pd.Series(),
    #     'fty': pd.Series(),
    #     'mass': pd.Series()
    #     }

    return System(params,
                  init = init,
                  area = area,
                  vehicle = Vehicle("./config/atlas_v_version_551.jsonc"),
                  telemetry=telemetry
                  )

def calculate_all(system, t, x, y, vx, vy):
    V = Vector(vx, vy)
    P = Vector (x, y)

    gnc = get_gnc(t, P, V, system)

    mass, thrust_mag = system.vehicle.get_tick_info(t, gnc)

    f_drag = drag_force(V, P, system)
    a_drag = f_drag / mass

    f_thrust = thrust_mag * gnc.facing
    a_thrust = f_thrust / mass
    
    G = calc_gravity(P, system)
    A = G + a_drag + a_thrust

    return Params(
        acceleration = Params(
            total = A,
            gravity = G,
            drag = a_drag,
            trust = a_thrust,
        ),
        mass = mass,
        forces = Params(
            drag = f_drag,
            trust = f_thrust
        )
    )




def slope_func(t, state, system):
    x, y, vx, vy = state

    calculations = calculate_all(system, t, x, y, vx, vy)
    A = calculations.acceleration.total

    # save telemetry
    system.telemetry['t'].append(t)
    system.telemetry['x'].append(x)
    system.telemetry['y'].append(y)
    # system.telemetry['ax'][t] = calculations.acceleration.total.x
    # system.telemetry['ay'][t] = calculations.acceleration.total.y
    # system.telemetry['gx'][t] = calculations.acceleration.gravity.x
    # system.telemetry['gy'][t] = calculations.acceleration.gravity.y
    # system.telemetry['trust_a'][t] = vector_mag(calculations.acceleration.trust)
    # system.telemetry['trust_f'][t] = vector_mag(calculations.forces.trust)
    # system.telemetry['aty'][t] = calculations.acceleration.trust.y
    # system.telemetry['atx'][t] = calculations.forces.trust.x
    # system.telemetry['aty'][t] = calculations.forces.trust.y
    # system.telemetry['mass'][t] = calculations.mass
    
    return vx, vy, A.x, A.y

def event_func(t, state, system):
    x, y, vx, vy = state
    height_above_earth = vector_mag(Vector(x, y)) - (0.5 * system.earth_diameter)
    return height_above_earth if t > 0 else 1

def run_sim():
    system = make_system(params)

    results, details = run_solve_ivp(system, slope_func,
                                 events=event_func)
    print(details.message)

    tel2 = {
    'x': system.telemetry['x'],
    'y': system.telemetry['y']
    }

    # system.telemetry['ax'] = system.telemetry['ax'].sort_index()
    # system.telemetry['ay'] = system.telemetry['ay'].sort_index()
    # system.telemetry['gx'] = system.telemetry['gx'].sort_index()
    # system.telemetry['gy'] = system.telemetry['gy'].sort_index()
    # system.telemetry['trust_a'] = system.telemetry['trust_a'].sort_index()
    # system.telemetry['trust_f'] = system.telemetry['trust_f'].sort_index()
    # system.telemetry['aty'] = system.telemetry['aty'].sort_index()
    # system.telemetry['atx'] = system.telemetry['atx'].sort_index()
    # system.telemetry['aty'] = system.telemetry['aty'].sort_index()
    # system.telemetry['mass'] = system.telemetry['mass'].sort_index()
    # telemetry_df = pd.DataFrame(data=system.telemetry)

    telemetry_df = pd.DataFrame(data=tel2, index=system.telemetry['t']).sort_index()

    return (results, telemetry_df)