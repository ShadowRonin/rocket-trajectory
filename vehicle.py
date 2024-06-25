import json
from vehicle_stage import VehicleStage

def createStage(c):
    return VehicleStage(
        c['name'],
        c['stage'],
        c['max_thrust'],
        c['burn_time'],
        c['start_burn_at'] if hasattr(c, 'start_burn_at') else 0,
        c['total_mass'],
        c['propellent_mass']
        )

class Vehicle:
    def __init__ (self, path_to_config):
        f = open(path_to_config)
        config = json.load(f)

        self.stages = list(map(createStage, config["stages"]))
        self.current_stage = 0
        self.max_stage = max(map(lambda s : s.stage, self.stages))
        self.update_stages(0)
        self.payload_mass = config["payload"]

    def get_mass(self, t):
        return self.payload_mass + sum(map(lambda s : 0 if s.has_staged(t) else s.get_mass(t), self.stages))
    
    def get_trust(self, t):
        return sum(map(lambda s : 0 if s.has_staged(t) else s.get_thrust_force(t), self.stages))
    
    def update_stages(self, t):
        update_stage = True
        for s in self.stages:
            if s.stage <= self.current_stage:
                if not s.has_staged(t):
                    update_stage = False

        if update_stage:
            self.current_stage += 1
            for s in self.stages:
                if s.stage == self.current_stage:
                    s.start_burn(t)

    def get_tick_info(self, t):
        self.update_stages(t)
        return (self.get_mass(t), self.get_trust(t))

if __name__ == "__main__":
    v = Vehicle("./config/atlas_v_version_551.jsonc")
    print(v)
        