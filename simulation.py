import matplotlib.pyplot as plt
import numpy as np
import solar

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

class Spacecraft:
    def __init__(self, state, planet_trajectories):  # state: (time, x, y, z, vx, vy, vz, fired)
        self.time = state[0]
        self.pos = state[1:4]
        self.vel = state[4:7]
        self.fired = state[7]
        self.planet_trajectories = planet_trajectories
        self.planets = planet_trajectories.keys()
        
    def update_acc(self, action_acc):
        norm_pos = np.linalg.norm(self.pos)
        self.acc = -GM_SUN / (norm_pos * norm_pos * norm_pos) * self.pos + action_acc
        for planet in self.planets:
            pos = self.planet_trajectories[planet][self.time][0:3]
            r = pos - self.pos
            r_norm = np.linalg.norm(r)
            if r_norm < 1e3:
                print(f"too close to {planet} with distance {r_norm}")
                continue
            self.acc += planet_GM[planet] / (r_norm * r_norm * r_norm) * r
            
    def step(self, action, dt):
        if self.fired == 0:
            if action[3] > 0:
                self.fired = 1
                state = self.planet_trajectories["earth"][self.time]
                self.pos = state[0:3].copy()
                self.vel = state[3:6].copy()
                self.pos += 1e5 * self.pos / np.linalg.norm(self.pos)
                # plt.scatter([self.pos[0]], [self.pos[1]], c='red', s=10)
            else:
                pos0 = self.pos.copy()
                vel0 = self.vel.copy()
                state = self.planet_trajectories["earth"][self.time]
                self.pos = state[0:3].copy()
                self.vel = state[3:6].copy()
                return Spacecraft(np.concatenate(([self.time - 1], pos0, vel0, [self.fired])), self.planet_trajectories)
        
        pos0 = self.pos.copy()
        vel0 = self.vel.copy()
        acc = action[0:3]
        self.update_acc(acc)
        self.vel += self.acc * dt / 2
        self.pos += self.vel * dt
        self.update_acc(acc)
        self.vel += self.acc * dt / 2
        self.time += 1
        return Spacecraft(np.concatenate(([self.time - 1], pos0, vel0, [self.fired])), self.planet_trajectories)


if __name__ == "__main__":
    trajectory_data = solar.get_trajectory()
    ax = plt.subplot(projection='3d')
    start_time = 2433283
    dt = 86400
    spacecraft = Spacecraft(np.concatenate(([start_time], trajectory_data["earth"][start_time], [0])), trajectory_data)
    traj = []
    for i in range(1000):
        spacecraft.step(np.array([0, 0, 0, 1]), dt)
        traj.append(spacecraft.pos.copy())
    traj = np.array(traj)

    solar.plot_trajectory(ax, traj, 5e9)
    solar.plot_planet_trajectory(ax, trajectory_data, planet_name, 5e9)
    plt.legend()
    plt.show()