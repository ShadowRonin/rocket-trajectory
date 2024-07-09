
class VehicleStage:
    def __init__(
            self,
            name,
            stage,
            max_thrust,
            burn_time,
            start_burn_at,
            total_mass,
            propellent_mass
            ):
        self.name = name
        self.stage = stage
        
        self.max_thrust = max_thrust
        self.burn_time = burn_time
        self.start_burn_at = start_burn_at

        self.propellent_mass = propellent_mass
        self.total_mass = total_mass

        self.is_burning = False
        self.burn_started_at = 0
        self.cumulative_burn_time = 0

    def get_burn_length(self, t):
        current_burn_length = t - self.burn_started_at if self.is_burning else 0
        return self.cumulative_burn_time + current_burn_length
    
    def start_burn(self, t):
        if not self.is_burning and t >= self.start_burn_at:
            print(self.name, " burn start: ", t)
            self.is_burning = True
            self.burn_started_at = t

    def stop_burn(self, t):
        if self.is_burning and t >= self.start_burn_at:
            print(self.name, " burn stop: ", t)
            self.is_burning = False
            self.cumulative_burn_time += t - self.burn_started_at

    def get_thrust_force(self, t):
        burn_length = self.get_burn_length(t)

        if self.is_burning and burn_length < self.burn_time:
            return self.max_thrust * 1000 # convert kN to N
        else:
            return 0

    def get_mass(self, t):
        if self.is_burning:
            burn_length = self.get_burn_length(t)

            if burn_length < self.burn_time:
                used_propellent_mass = self.propellent_mass * (burn_length / self.burn_time)
                return self.total_mass - used_propellent_mass
            else:
                return self.total_mass - self.propellent_mass
        else:
            return self.total_mass
    
    def has_staged(self, t):
        burn_length = self.get_burn_length(t)
        if burn_length > self.burn_time:
            self.stop_burn(t)
            return True
        else:
            return False