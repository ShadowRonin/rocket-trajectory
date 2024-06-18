def calc_mass(t, system):
    burn_time, mass, propellent_mass = system.burn_time, system.mass, system.propellent_mass
    used_propellent_mass = propellent_mass * (t / burn_time) if t < burn_time else propellent_mass
    return mass - used_propellent_mass