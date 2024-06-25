from modsim import *

def get_rho(height):
    if height >= 80000:
        return 0.00001846
    elif height >= 70000:
        return 0.00008283
    elif height >= 60000:
        return 0.0003097
    elif height >= 50000:
        return 0.001027
    elif height >= 40000:
        return 0.003996
    elif height >= 30000:
        return 0.01841
    elif height >= 25000:
        return 0.04008
    elif height >= 20000:
        return 0.08891
    elif height >= 15000:
        return 0.1948
    elif height >= 10000:
        return 0.4135
    elif height >= 9000:
        return 0.4671
    elif height >= 8000:
        return 0.5258
    elif height >= 7000:
        return 0.5900
    elif height >= 6000:
        return 0.6601
    elif height >= 5000:
        return 0.7364
    elif height >= 4000:
        return 0.8194
    elif height >= 3000:
        return 0.9093
    elif height >= 2000:
        return 1.007
    elif height >= 1000:
        return 1.112
    elif height >= 0:
        return 1.225
    else:
        return 1.347
    
def drag_force(V, P, system):
    C_d, area = system.C_d, system.area

    height_above_earth = vector_mag(P) - (system.earth_diameter / 2)
    rho = get_rho(height_above_earth)
    
    drag_mag = rho * vector_mag(V)**2 * C_d * area / 2
    direction = -1 * vector_hat(V)
    f_drag = drag_mag * direction
    return f_drag