import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

def State(**variables):
    """Contains the values of state variables."""
    return pd.Series(variables, name='state')

mass = 0.0025      # kg
diameter = 0.019   # m
rho = 1.2          # kg/m**3
g = 9.8            # m/s**2
v_init = 0         # m / s
v_term = 18        # m / s
height = 381       # m
t_end = 30         # s

class System():
    def __init__(self, init,area,C_d,mass,rho,g,t_end):
        self.init=init
        self.area=area
        self.C_d=C_d
        self.mass=mass
        self.rho=rho
        self.g=g
        self.t_end=t_end

def make_system():
    init = State(y=height, v=v_init)

    area = np.pi * (diameter/2)**2

    C_d = (2 * mass * g / 
           (rho * area * v_term**2))

    return System(init=init,
                  area=area,
                  C_d=C_d,
                  mass=mass,
                  rho=rho,
                  g=g,
                  t_end=t_end)

system = make_system()

def slope_func(t, state, system):
    y, v = state
    rho, C_d, area = system.rho, system.C_d, system.area
    mass, g = system.mass, system.g
    
    f_drag = rho * v**2 * C_d * area / 2
    a_drag = f_drag / mass
    
    dydt = v
    dvdt = -g + a_drag
    
    return dydt, dvdt

def event_func(t, state, system):
    y, v = state
    return y

result = solve_ivp(slope_func, [0, system.t_end], system.init,
                      args=[system], events=[event_func])

plt.figure(figsize = (12,4))

plt.subplot(1,2,1)
plt.plot(result.t, result.y[0])
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')

plt.subplot(1,2,2)
plt.plot(result.t, result.y[1])
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')


plt.tight_layout()
plt.show()
