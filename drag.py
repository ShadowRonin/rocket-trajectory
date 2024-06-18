from modsim import *

def get_rho(y):
    if y >= 80000:
        return 0.00001846
    elif y >= 70000:
        return 0.00008283
    elif y >= 60000:
        return 0.0003097
    elif y >= 50000:
        return 0.001027
    elif y >= 40000:
        return 0.003996
    elif y >= 30000:
        return 0.01841
    elif y >= 25000:
        return 0.04008
    elif y >= 20000:
        return 0.08891
    elif y >= 15000:
        return 0.1948
    elif y >= 10000:
        return 0.4135
    elif y >= 9000:
        return 0.4671
    elif y >= 8000:
        return 0.5258
    elif y >= 7000:
        return 0.5900
    elif y >= 6000:
        return 0.6601
    elif y >= 5000:
        return 0.7364
    elif y >= 4000:
        return 0.8194
    elif y >= 3000:
        return 0.9093
    elif y >= 2000:
        return 1.007
    elif y >= 1000:
        return 1.112
    elif y >= 0:
        return 1.225
    else:
        return 1.347
    
def drag_force(V, y, system):
    C_d, area = system.C_d, system.area
    rho = get_rho(y)
    
    mag = rho * vector_mag(V)**2 * C_d * area / 2
    direction = -vector_hat(V)
    f_drag = mag * direction
    return f_drag