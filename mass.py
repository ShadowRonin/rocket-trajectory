def calc_mass(t, system):
    burn_time, mass, propellent_mass = system.burn_time, system.mass, system.propellent_mass
    used_propellent_mass = propellent_mass * (t / burn_time) if t < burn_time else propellent_mass
    return mass - used_propellent_mass

if __name__ == "__main__":
    from modsim import Params
    print(calc_mass(5, Params(
        burn_time = 10,
        mass = 46697,
        propellent_mass = 42630,
    )))