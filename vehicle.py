import json
from vehicle_stage import VehicleStage
from event import Event

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
        self.payload_mass = config["payload"]
        self.number_of_stages = config["number_of_stages"]

    def get_mass(self, t):
        return self.payload_mass + sum(map(lambda s : 0 if s.has_staged(t) else s.get_mass(t), self.stages))
    
    def get_trust(self, t):
        total_kN = sum(map(lambda s : 0 if s.has_staged(t) else s.get_thrust_force(t), self.stages))
        total_N = total_kN * 1000
        return total_N

    def update_stages(self, t, gnc):
        stage_events = []

        if False and gnc.has_reached_orbit:
            for s in self.stages:
                s.stop_burn(t)
        elif self.number_of_stages + 1 > self.current_stage:
            update_stage = True
            for s in self.stages:
                if s.stage <= self.current_stage:
                    if not s.has_staged(t):
                        update_stage = False

            if update_stage:
                self.current_stage += 1
                stage_events.append(Event(t, f'Stage {self.current_stage} start'))
                for s in self.stages:
                    if s.stage == self.current_stage:
                        s.start_burn(t)

        return stage_events

    def get_tick_info(self, t, gnc):
        staging_events = self.update_stages(t, gnc)
        return (self.get_mass(t), self.get_trust(t), staging_events)

if __name__ == "__main__":
    v = Vehicle("./config/atlas_v_version_551.jsonc")
    print(v)
        