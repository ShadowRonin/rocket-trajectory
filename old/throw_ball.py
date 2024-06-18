import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

# All corods are [x,y], m
p0 = [0.0, 0.0] # Starting position

# Starting velocity, m/s
Vx0 = 1.0
Vy0 = 1.0

g = 9.8 # acceleration of gravity, m/s^2
Cd = 0.5 # coefficient of drag of a sphere
rho = 1.225 # density of the air at standard temp and pressure, mg/m^3

m = 1.0 # mass of sphere, kg
diameter = 0.05 # diameter of sphere in m
# Note: area is supposed to be "area of the object facing the fluid"
# So maybe we need to do something more then just the area of the sphere?
# like idk half the area since only half will be facing the direction fo travel?
A = 4 * np.pi * np.square(diameter / 2)

Vt = np.sqrt((2 * m * g) / (Cd * A * rho)) # terminal V
Vtsq = np.square(Vt)

def F(t,s):
    # Per nasa? https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/flight-equations-with-drag/
    Vt = np.sqrt((2 * m * g) / (Cd * A * rho)) # terminal V
    Vtsq = np.square(Vt)
    Vx = (Vtsq * Vx0) / (Vtsq + g * Vx0 * t)
    x = (Vtsq / g) * np.log((Vtsq + g * Vx0 * t) / Vtsq)

    Vy = Vt * ((Vy0 - Vt * np.tan(t * g / Vt)) / (Vt + Vy0 * np.tan(t * g / Vt)))
    y = (Vtsq / 2 * g) * np.log((np.square(Vy0) + Vtsq) / (np.square(Vy) + Vtsq))

    # BRUTE
    # x_prev= s[0]
    # y_prev= s[1]
    # Vx_prev = s[1]
    # Vy_prev = s[2]
    # V_mag = np.sqrt(Vx_prev**2 + Vy_prev**2)
    # V_ang = Vx_prev / Vy_prev
    # t_prev = s[4]
    # dt = t - t_prev

    # F_D_ang = (2 * np.pi) - V_ang
    # F_D = 0.5 * Cd * rho * A * np.square(V_mag)
    # Fx_D = np.cos(F_D_ang) * F_D
    # Fy_D = np.sin(F_D_ang) * F_D
    # check = np.sqrt(Fx_D**2 * Fy_D**2)
    # print('F_D: ', F_D)
    # print('check: ', check)

    # Ax = Fx_D / m
    # Ay = (-1 * g) * Fy_D / m

    # dv_x = Ax * dt
    # dv_y = Ay * dt
    # Vx = Vx_prev + dv_x
    # Vy = Vy_prev + dv_y

    # dx = Vx * dt
    # dy = Vy * dt

    # x = x_prev + dx
    # y = y_prev + dy    

    # BRUTE Array
    # p_prev = np.array([s[0], s[1]])
    # V_prev = np.array([s[1], s[2]])
    # V_mag = np.sqrt(V_prev[0]**2 + V_prev[1]**2)
    # V_unit = np.array([V_prev[0] / V_mag, V_prev[1] / V_mag])
    # t_prev = s[4]
    # dt = t - t_prev

    # F_D = 0.5 * Cd * rho * A * np.square(V_prev)

    # A_D = -1 * F_D / m
    # A_g = np.array([0.0, -g])
    # A_total = A_D + A_g

    # dv = A_total * dt
    # V = V_prev + dv

    # dp = V * dt
    # p = p_prev + dp

    # x = p[0]
    # y = p[1]
    # Vx = V[0]
    # Vy = V[1]

    return [x, y, Vx, Vy, t]

t_max = 10
t_eval = np.arange(0, t_max, 0.1)
sol = solve_ivp(F, [0, t_max], [0, 0, Vx0, Vy0, 0], method="LSODA")
# sol = solve_ivp(F, [0, t_max], [0, 0, Vx0, Vy0], t_eval=t_eval)

print(np.max(sol.y[0]))
print(np.min(sol.y[0]))
print(np.max(sol.y[1]))
print(np.min(sol.y[1]))


plt.figure(figsize = (12,4))

plt.subplot(1,2,1)
plt.plot(sol.t, sol.y[0])
plt.xlabel('t')
plt.ylabel('x(t)')

plt.subplot(1,2,2)
plt.plot(sol.t, sol.y[2])
plt.xlabel('t')
plt.ylabel('v^x(t)')


# plt.figure(figsize = (12,4))

# plt.subplot(1,2,1)
# plt.plot(sol.t, sol.y[1])
# plt.xlabel('t')
# plt.ylabel('y(t)')

# plt.subplot(1,2,2)
# plt.plot(sol.t, sol.y[3])
# plt.xlabel('t')
# plt.ylabel('v^y(t)')

# plt.figure(figsize = (12,4))

# plt.subplot(1,2,1)
# plt.plot(sol.y[0], sol.y[1])
# plt.xlabel('x')
# plt.ylabel('y')

plt.tight_layout()
plt.show()