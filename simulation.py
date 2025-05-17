import matplotlib.pyplot as plt
import numpy as np
import solar

G = 6.6743e-20
M_SUN = 1.9884e30
GM_SUN = G * M_SUN

planet_name = [
"mars",
"jupiter",
"saturn",
"uranus",
"neptune",
"earth"
]

mass = {
    "mars": 6.4185e23,
    "jupiter": 1.8982e27,
    "saturn": 5.6832e26,
    "uranus": 8.6811e25,
    "neptune": 1.0241e26,
    "earth": 5.9722e24
}

class Planet:
    def __init__(self, name, mass, pos, vel, vector_count, record_size, attracting=False):  #  vector_count: how many vectors can be saved
        self.name = name
        self.Gmass = G * mass
        self.mass = mass
        self.massinv = 1 / mass
        self.pos = np.zeros((vector_count, 3))
        self.pos[0] = pos
        self.vel = np.zeros((vector_count, 3))
        self.vel[0] = vel
        self.acc = np.zeros((vector_count, 3))
        self.attracting = attracting
        self.trajectories = np.zeros((record_size, 3))

    def add_sun_acc(self, acc_index, pos_index):
        r = -self.pos[pos_index]
        r_norm = np.linalg.norm(r)
        acc = GM_SUN / (r_norm * r_norm * r_norm) * r
        self.acc[acc_index] += acc
        # print(np.linalg.norm(acc), r_norm)

    def add_attracted_acc(self, source, acc_index, pos_index):
        r = source.pos[pos_index] - self.pos[pos_index]
        r_norm = np.linalg.norm(r)
        acc = source.Gmass / (r_norm * r_norm * r_norm) * r
        self.acc[acc_index] += acc
        return acc
    
    def reset_acc(self, index):
        self.acc[index] = np.zeros(3)
    
class SolarSim:
    def __init__(self, all_planets, step_count, dt):
        self.attractor = []
        self.affected = []
        for planet in all_planets:
            if planet.attracting:
                self.attractor.append(planet)
            else:
                self.affected.append(planet)
        self.all_planets = all_planets
        self.step_count = step_count
        self.dt = dt
        self.gen = 0

    def update_acceleration(self, acc_index, pos_index):
        # affected attracted by sun
        for target in self.affected:
            target.reset_acc(acc_index)
            target.add_sun_acc(acc_index, pos_index)
        # attractor attracting all
        # attractor attracted by sun
        for i, source in enumerate(self.attractor):
            source.reset_acc(acc_index)
            source.add_sun_acc(acc_index, pos_index)
            for target in self.affected:
                target.add_attracted_acc(source, acc_index, pos_index)
            for j in range(i + 1, len(self.attractor)):
                target = self.attractor[j]
                added_acc = target.add_attracted_acc(source, acc_index, pos_index)
                source.acc[acc_index] -= added_acc * source.massinv * target.mass  # here is wrong

    def add_trajectory(self, index):
        for planet in all_planets:
            # print(planet.pos[0])
            planet.trajectories[self.gen] = planet.pos[index]

    def Leapfrog_update(self):
        for planet in all_planets:
            # print(planet.vel[0], planet.acc[0])
            planet.vel[0] += planet.acc[0] * self.dt / 2
            planet.pos[0] += planet.vel[0] * self.dt
            # print(planet.pos[0])
        self.update_acceleration(0, 0)
        for planet in all_planets:
            planet.vel[0] += planet.acc[0] * self.dt / 2

    def run_Leapfrog(self):
        for _ in range(self.step_count):
            self.Leapfrog_update()
            self.add_trajectory(0)
            self.gen += 1

    def get_trajectory(self, index):
        trajectories = dict()
        for planet in self.all_planets:
            trajectories[planet.name] = planet.trajectories
        # print(trajectories)
        return trajectories


real_trajectories = solar.get_trajectory(planet_name)
init = solar.get_init_condition(planet_name)

time_span = 365 * 86400 * 2.4
dt = 10000
step_count = int(time_span / dt)

all_planets = []
for planet in planet_name:
    pos = init[planet][0]
    vel = init[planet][1]
    planet_obj = Planet(planet, mass[planet], pos, vel, 4, step_count, attracting=True)
    all_planets.append(planet_obj)
    if planet == "earth":
        earth_pos = pos.copy()
        earth_vel = vel.copy()

spacecraft_init_vel = 9.5 * earth_vel / np.linalg.norm(earth_vel) + earth_vel
spacecraft = Planet("spacecraft", 1, earth_pos, spacecraft_init_vel, 4, step_count)
all_planets.append(spacecraft)
planet_name.append("spacecraft")

solar_sim = SolarSim(all_planets, step_count, dt)
solar_sim.run_Leapfrog()
trajectories = solar_sim.get_trajectory(0)

# print(trajectories)

solar.plot_trajectory(trajectories, planet_name, 8e8)
# solar.plot_trajectory(real_trajectories, planet_name, 5e9)
plt.legend()
plt.show()