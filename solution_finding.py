import gym
import numpy as np
import matplotlib.pyplot as plt
import solar
from simulation import Spacecraft

class SpacecraftEnv(gym.Env):
    def __init__(self, trajectories, dt):
        self.trajectories = trajectories
        self.dt = dt
        self.acc_lim = 1e-6
        self.end_time = 2457023
        self.clear_data()
    
    def step(self, action):  # actoin: (ax, ay, az, fire[>0 to fire])
        self.action = action
        self.spacecraft_history.append(self.spacecraft.step(action, self.dt))
        if self.spacecraft.time >= self.end_time or np.linalg.norm(self.spacecraft.pos) > 5e9:
            self.done = True
        reward = self.get_reward()
        state = self.get_obs()
        return state, reward, self.done, {}
    
    def reset(self):
        self.clear_data()
        return
    
    def get_obs(self):
        return np.concatenate(([self.spacecraft.time], self.spacecraft.pos, self.spacecraft.vel, [self.spacecraft.fired]))
    
    def get_reward(self):
        reward = np.log(np.linalg.norm(self.spacecraft.pos)) * 100
        acc = np.linalg.norm(self.action[0:3])
        vel = np.linalg.norm(self.spacecraft.vel)
        if acc > self.acc_lim:
            return -1e10
        
        reward -= acc * 1e6
        if not self.done:
            reward += vel
        else:
            reward -= (self.spacecraft.time - start_time) / 10
        
        return reward
    
    def clear_data(self):
        state = np.concatenate(([start_time], self.trajectories["earth"][start_time], [0]))
        self.spacecraft = Spacecraft(state, self.trajectories)
        self.spacecraft_history = []
        self.action_history = []
        self.done = False
    
start_time = 2433283
dt = 86400