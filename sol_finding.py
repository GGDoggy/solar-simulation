import gymnasium as gym
from gymnasium import spaces
import numpy as np
import matplotlib.pyplot as plt
import solar
from simulation import Spacecraft
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3 import SAC, A2C
import time

class SpacecraftEnv(gym.Env):
    def __init__(self, trajectories, dt):
        super().__init__()
        self.trajectories = trajectories
        self.dt = dt
        self.acc_lim = 5e-7
        self.start_time = 2433283
        self.end_time = 2457023
        self.clear_data()
        self.observation_space = spaces.Box(low=-np.inf,high=np.inf,shape=(26, ), dtype=np.float64)
        self.action_space = spaces.Box(low=-1, high=1, shape=(7, ), dtype=np.float64)
        self.acc = 0
    
    def step(self, action):  # actoin: (ax, ay, az, fire[>0 to fire], init_vel)
        self.action = action * self.acc_lim
        self.state_history.append(self.spacecraft.step(self.action, self.dt))
        self.action_history.append(self.action)
        self.acc = np.linalg.norm(self.action[0:3])
        if self.start_flying:
            self.flying_time += 1
        else:
            if action[3] > 0.99:
                self.start_flying = True
                self.delay_time = self.spacecraft.time - self.start_time
        if self.spacecraft.time >= self.end_time or self.spacecraft.too_close or self.flying_time > self.maxtime:
            self.truncated = True
        if np.linalg.norm(self.spacecraft.pos) > 5e9:
            self.done = True
        state = self.get_obs()
        reward = self.get_reward()
        return state, reward, self.done, self.truncated, {}
    
    def reset(self, seed=0):
        self.clear_data()
        self.state = self.get_obs()
        return self.state, {}
    
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
        pos = np.linalg.norm(self.spacecraft.pos[0:2]) / 1e8
        vel = np.linalg.norm(self.spacecraft.vel)
        self.maxpos = max(pos, self.maxpos)
        self.maxvel = max(vel, self.maxvel)

        if not self.start_flying:
            reward = 0

        # if pos < 1:
        #     reward = -np.arctan(1 / pos) * 20
        if self.stage == 0:
        # if pos < 2.5:
            disp = self.state[11:14] - self.state[1:4]
            disp = np.linalg.norm(disp) / 1e8
            # toward_vel = np.dot(self.state[4:7], disp) / np.linalg.norm(disp)
            # reward = pos + np.arctan(1 / np.linalg.norm(disp)) * 6
            reward = (5 - disp)**2 + self.coll_dealing(disp)
        elif self.stage == 1:
        # elif pos < 8.2:
            disp = self.state[14:17] - self.state[1:4]
            disp = np.linalg.norm(disp) / 1e8
            # toward_vel = np.dot(self.state[4:7], disp) / np.linalg.norm(disp)
            # reward = pos + np.arctan(1 / np.linalg.norm(disp)) * 16
            reward = (16 - disp)**2 + self.col_max_rew + self.coll_dealing(disp) - self.flying_time

        else:
            reward = np.linalg.norm(self.spacecraft.pos)

        if self.colliding:
            self.col_max_rew = max(self.col_max_rew, reward)

        # for planet in self.spacecraft.distance:
        #     dis = self.spacecraft.distance[planet]
            

        # vel = np.linalg.norm(self.spacecraft.vel)
        # z = self.spacecraft.pos[2] / 1e5
        # r_vel = np.dot(self.spacecraft.pos, self.spacecraft.vel) / pos
        # reward = pos
        # if r_vel < 0:
        #     reward -= r_vel * r_vel * r_vel
        # if self.spacecraft.fired == 0:
        #     reward -= (self.spacecraft.time - self.start_time)
        # if self.done:
        #     reward += pos**2 * 1e2
        # elif self.spacecraft.fired == 1:
        #     reward -= self.flying_time * 1e-3
        self.reward_sum += reward
        return reward
    
    def clear_data(self):
        state = np.concatenate(([self.start_time], self.trajectories["earth"][self.start_time], [0]))
        self.spacecraft = Spacecraft(state, self.trajectories)
        self.state_history = []
        self.action_history = []
        self.done = False
        self.truncated = False
        self.flying_time = 0
        self.start_flying = False
        self.reward_sum = 0
        self.stage = 0
        self.maxpos = 0
        self.maxvel = 0
        self.maxtime = 300
        self.colliding = False
        self.col_max_rew = 0
        self.mindisp = np.inf
        self.delay_time = 0

    def coll_dealing(self, disp):
        rew = 0
        self.mindisp = min(self.mindisp, disp)
        if disp < 1e-3:
            self.colliding = True
        elif disp < 1.8:
            rew = np.arctan(0.33 / disp) * 1e2
        if self.colliding and disp > 1e-3:
            self.colliding = False
            self.maxtime += 1000
            self.stage += 1
            self.mindisp = np.inf
        return rew
    
class TensorboardCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        self.logger.record("rollout/reward_sum", self.model.env.get_attr("reward_sum")[0])
        self.logger.record("rollout/stage", self.model.env.get_attr("stage")[0])
        self.logger.record("rollout/maxpos", self.model.env.get_attr("maxpos")[0])
        self.logger.record("rollout/maxvel", self.model.env.get_attr("maxvel")[0])
        self.logger.record("rollout/mindisp", self.model.env.get_attr("mindisp")[0])
        self.logger.record("rollout/delay_time", self.model.env.get_attr("delay_time")[0])
        return True


start_time = 2433283
end_time = 2457023
dt = 86400

trajectory_data = solar.get_trajectory()
# env = SpacecraftEnv(trajectory_data, dt)
env = DummyVecEnv([lambda: SpacecraftEnv(trajectory_data, dt)])
# check_env(env)

# time_rec = time.time()
# print("start learning")
# model = A2C("MlpPolicy", env, verbose=1, learning_rate=1e-5, tensorboard_log="tensorboard", device="cpu")
# # model = A2C.load("sac_spacecraft", env, device="cpu")
# model.learn(total_timesteps=200_000, callback=TensorboardCallback(verbose=1), reset_num_timesteps=False)
# model.save("sac_spacecraft")
# del model
# print(f"finish learning in {time.time() - time_rec} s")

time_rec = time.time()
# eval_env = DummyVecEnv([lambda: SpacecraftEnv(trajectory_data, dt)])
eval_env = SpacecraftEnv(trajectory_data, dt)
model = A2C.load("sac_spacecraft", device="cpu")
print("start simulation")
obs = eval_env.reset()[0]
truncated = False
dones = False
while not truncated and not dones:
    action, _states = model.predict(obs)
    # print(action.shape)
    obs, rewards, dones, truncated, info = eval_env.step(action)
print(f"finish simultion in {time.time() - time_rec} s")

traj = np.array(eval_env.state_history)[:, 1:4]
ax = plt.subplot(projection='3d')
solar.plot_trajectory(ax, traj, 5e9)
solar.plot_planet_trajectory(ax, eval_env.trajectories, eval_env.trajectories.keys(), 5e9)
plt.show()



# python -m tensorboard.main --logdir=./