import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt
import solar
from simulation import Spacecraft
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3 import SAC

class SpacecraftEnv(gym.Env):
    def __init__(self, trajectories, dt):
        super().__init__()
        self.trajectories = trajectories
        self.dt = dt
        self.acc_lim = 1e-7
        self.start_time = 2433283
        self.end_time = 2457023
        self.clear_data()
        self.observation_space = spaces.Box(low=-np.inf,high=np.inf,shape=(26, ), dtype=np.float64)
        self.action_space = spaces.Box(low=-self.acc_lim, high=self.acc_lim, shape=(4, ), dtype=np.float64)
        self.record = []
        self.acc = 0
    
    def step(self, action):  # actoin: (ax, ay, az, fire[>0 to fire])
        self.action = action
        self.spacecraft_history.append(self.spacecraft.step(action, self.dt))
        self.action_history.append(action)
        self.acc = np.linalg.norm(self.action[0:3])
        if self.start_flying:
            self.flying_time += 1
        if self.spacecraft.time >= self.end_time or self.spacecraft.too_close or self.flying_time > 1000:
            self.truncated = True
        if np.linalg.norm(self.spacecraft.pos) > 5e9:
            self.done = True
        reward = self.get_reward()
        state = self.get_obs()
        return state, reward, self.done, self.truncated, {}
    
    def reset(self, seed=0):
        self.clear_data()
        return self.get_obs(), {}
    
    def get_obs(self):  # obs: (time, x, y, z, vx, vy, vz, fired, all planets' pos)
        return np.concatenate(([self.spacecraft.time], self.spacecraft.pos, self.spacecraft.vel, [self.spacecraft.fired], 
                               self.trajectories["earth"][self.spacecraft.time][0:3],
                               self.trajectories["mars"][self.spacecraft.time][0:3],
                               self.trajectories["jupiter"][self.spacecraft.time][0:3],
                               self.trajectories["saturn"][self.spacecraft.time][0:3],
                               self.trajectories["uranus"][self.spacecraft.time][0:3],
                               self.trajectories["neptune"][self.spacecraft.time][0:3]))
    
    def get_reward(self):
        if self.truncated:
            return -1e10
        reward = np.linalg.norm(self.spacecraft.pos) / 1e8
        vel = np.linalg.norm(self.spacecraft.vel)
        if not self.done:
            if self.spacecraft.fired == 1:
                reward += vel / 100
            else:
                reward -= self.flying_time * 1e-4
        return reward
    
    def clear_data(self):
        state = np.concatenate(([self.start_time], self.trajectories["earth"][self.start_time], [0]))
        self.spacecraft = Spacecraft(state, self.trajectories)
        self.spacecraft_history = []
        self.action_history = []
        self.done = False
        self.truncated = False
        self.flying_time = 0
        self.start_flying = False
    
start_time = 2433283
end_time = 2457023
dt = 86400

trajectory_data = solar.get_trajectory()
env = SubprocVecEnv([SpacecraftEnv(trajectory_data, dt) for _ in range(4)])
# check_env(env)

model = SAC("MlpPolicy", env, verbose=1, learning_rate=0.0003)
model.learn(total_timesteps=1)
model.save("sac_spacecraft")
del model

eval_env = SpacecraftEnv(trajectory_data, dt)
model = SAC.load("sac_spacecraft")
obs = eval_env.reset()[0]
truncated = False
done = False
while not truncated and not done:
    action, _states = model.predict(obs)
    obs, rewards, dones, truncated, info = eval_env.step(action)
    # print(obs, action)

traj = []
for spacecraft in eval_env.spacecraft_history:
    traj.append(spacecraft.pos)
traj = np.array(traj)
ax = plt.subplot(projection='3d')
# print(traj)
solar.plot_trajectory(ax, traj, 5e9)
solar.plot_planet_trajectory(ax, eval_env.trajectories, eval_env.trajectories.keys(), 5e9)
plt.show()