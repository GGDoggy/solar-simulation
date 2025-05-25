import matplotlib.pyplot as plt
import numpy as np
import solar
import time

G = 6.6743e-20
M_SUN = 1.9884e30
GM_SUN = G * M_SUN

planet_name = [
"earth",
"mars",
"jupiter",
"saturn",
"uranus",
"neptune"
]

planet_GM = {
    "mars": 6.4185e23 * G,
    "jupiter": 1.8982e27 * G,
    "saturn": 5.6832e26 * G,
    "uranus": 8.6811e25 * G,
    "neptune": 1.0241e26 * G,
    "earth": 5.9722e24 * G
}

planet_radius = {
    "mars": 3376.2,
    "jupiter": 66854,
    "saturn": 58232,
    "uranus": 25362,
    "neptune": 24622,
    "earth": 6371,
    "sun": 5e7
}


class Spacecraft:
    def __init__(self, state, planet_trajectories):  # state: (time, x, y, z, vx, vy, vz, fired)
        self.time = state[0]
        self.pos = state[1:4]
        self.vel = state[4:7]
        self.fired = state[7]
        self.planet_trajectories = planet_trajectories
        self.planets = list(planet_trajectories.keys())
        self.too_close = False
        self.distance = dict()
        self.time_list = list(planet_trajectories[self.planets[0]].keys())
        self.time_index = self.time_list.index(self.time)
        
    def update_acc(self, action_acc, close=False, targ=""):
        if close:
            norm_pos = np.linalg.norm(self.pos)
            self.acc = -GM_SUN / (norm_pos * norm_pos * norm_pos) * self.pos
            targ_prev_pos = self.planet_trajectories[targ][self.time_list[self.time_index - 1]][0:3]
            targ_next_pos = self.planet_trajectories[targ][self.time_list[self.time_index]][0:3]
            targ_step = (targ_next_pos - targ_prev_pos) / 3600
            targ_pos = targ_prev_pos + self.close_counter * targ_step
            disp = targ_pos - self.pos
            norm_disp = np.linalg.norm(disp)
            self.acc += planet_GM[targ] / (norm_disp * norm_disp * norm_disp) * disp
        else:
            norm_pos = np.linalg.norm(self.pos)
            if norm_pos < planet_radius["sun"]:
                print(f"too close to sun with distance {norm_pos}")
                self.too_close = True
                self.acc = -GM_SUN / (planet_radius["sun"] * planet_radius["sun"] * norm_pos) * self.pos + action_acc
            else:
                self.acc = -GM_SUN / (norm_pos * norm_pos * norm_pos) * self.pos + action_acc
            for planet in self.planets:
                pos = self.planet_trajectories[planet][self.time][0:3]
                r = pos - self.pos
                r_norm = np.linalg.norm(r)
                self.distance[planet] = r_norm
                if r_norm < planet_radius[planet]:
                    print(f"too close to {planet} with distance {r_norm}")
                    self.too_close = True
                    self.acc += planet_GM[planet] / (planet_radius[planet] * planet_radius[planet] * r_norm) * r
                else:
                    self.acc += planet_GM[planet] / (r_norm * r_norm * r_norm) * r
            
    def step(self, action, dt, close=False, targ=""):  # actoin: (ax, ay, az, fire[>0 to fire], init_vel)
        if close:
            pos0 = self.pos.copy()
            vel0 = self.vel.copy()
            acc = action[0:3] * 5.6e-6
            self.update_acc(acc, close=True, targ=targ)
            self.vel += self.acc * dt / 2
            self.pos += self.vel * dt
            self.update_acc(acc, close=True, targ=targ)
            self.vel += self.acc * dt / 2
            self.close_counter += 1
            return np.concatenate(([self.time - 1], pos0, vel0, [self.fired]))
        
        if not close:
            self.time_index += 1
            self.time = self.time_list[self.time_index]
            if self.fired == 0:
                if action[3] > 0:
                    self.fired = 1
                    state = self.planet_trajectories["earth"][self.time]
                    self.pos = state[0:3].copy()
                    self.vel = state[3:6].copy() + action[4:7] * 5.9
                    self.pos += 8e4 * self.pos / np.linalg.norm(self.pos)
                else:
                    pos0 = self.pos.copy()
                    vel0 = self.vel.copy()
                    state = self.planet_trajectories["earth"][self.time]
                    self.pos = state[0:3].copy()
                    self.vel = state[3:6].copy()
                    return np.concatenate(([self.time_list[self.time_index - 1]], pos0, vel0, [self.fired]))
            pos0 = self.pos.copy()
            vel0 = self.vel.copy()
            acc = action[0:3] * 5.6e-6
            self.update_acc(acc)
            self.vel += self.acc * dt / 2
            self.pos += self.vel * dt
            self.update_acc(acc)
            self.vel += self.acc * dt / 2
            return np.concatenate(([self.time - 1], pos0, vel0, [self.fired]))


if __name__ == "__main__":
    trajectory_data = solar.get_trajectory()
    ax = plt.subplot(projection='3d')
    start_time = 2433283
    dt = 86400
    spacecraft = Spacecraft(np.concatenate(([start_time], trajectory_data["earth"][start_time], [0])), trajectory_data)
    traj = []
    time_start = time.time()
    for i in range(1000):
        spacecraft.step(np.array([0, 0, 0, 1]), dt)
        traj.append(spacecraft.pos.copy())
    traj = np.array(traj)
    print(time.time() - time_start)

    solar.plot_trajectory(ax, traj, 1e9)
    solar.plot_planet_trajectory(ax, trajectory_data, planet_name, 1e9)
    plt.legend()
    plt.show()
