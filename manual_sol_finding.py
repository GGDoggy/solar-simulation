import numpy as np
import matplotlib.pyplot as plt
import json
import solar
from simulation import Spacecraft
from matplotlib.widgets import Button

def run_sim(spacecraft, fire_time, fire_delay, end_time, init_vel, acc_strategy, trajectory_data):
    acc_ptr = -1
    apply_time = fire_delay + 1
    action = np.zeros(7)
    traj_history = []
    vel_history = []
    acc_history = []
    have_acc = False
    close = False
    while spacecraft.time_index <= end_time:
        time = spacecraft.time_index
        if time == fire_time:
            action[3] = 1
            action[4:7] = init_vel
        if apply_time == 0:
            acc_ptr += 1
            apply_time = acc_strategy[acc_ptr][0]
            if acc_strategy[acc_ptr][1] == "wait":  # acc_strategy: [time, a1, a2, a3, targ_planet]
                have_acc = False
                close = False
                action[0:3] = [0, 0, 0]
            elif acc_strategy[acc_ptr][1] == "close":
                apply_time = 3600
                spacecraft.close_counter = 0
                close_targ = acc_strategy[acc_ptr][2]
                close = True
            elif acc_strategy[acc_ptr][2] == "z":
                action[0:3] = [0, 0, acc_strategy[acc_ptr][1]]
            else:
                have_acc = True
        if have_acc:
            planet_pos = trajectory_data[acc_strategy[acc_ptr][4]][spacecraft.time_list[time]][0:3]
            disp = planet_pos - spacecraft.pos
            vel = spacecraft.vel.copy()
            n_vel = vel / np.linalg.norm(vel)
            n_right = disp - np.dot(disp, n_vel) * n_vel
            n_right = n_right / np.linalg.norm(n_right)
            n_3 = np.linalg.cross(n_vel, n_right)
            acc = np.array(acc_strategy[acc_ptr][1:4])  # acc: (a_vel, a_to_planet\vel, a3)
            acc_xyz = np.matmul(np.linalg.inv(np.concatenate((n_vel, n_right, n_3), 0).reshape((3, 3)).T), acc.T).T
            action[0:3] = acc_xyz
        if close:
            spacecraft.step(action, close_dt, close=True, targ=close_targ)
        else:
            spacecraft.step(action, dt)
        if time > fire_time:
            traj_history.append(spacecraft.pos.copy())
            vel_history.append(spacecraft.vel.copy())
            acc_history.append(action[0:3].copy())
        apply_time -= 1
    return np.array(traj_history), np.array(vel_history), np.array(acc_history)



class Conditions:
    def __init__(self, fire_delay, run_time, trajectory_data, change_rate):
        self.start_time = 2433283
        self.fire_delay = fire_delay
        self.fire_time = fire_delay
        self.run_time = run_time
        self.end_time = self.fire_time + run_time
        self.trajectory_data = trajectory_data
        self.init_vel = np.zeros(3)
        self.get_acc()
        self.first = True
        self.change_rate = change_rate

    def get_condition(self):
        return self.fire_delay, self.fire_time, self.end_time, self.init_vel
    
    def add_fire_delay(self, event):
        self.fire_delay += self.change_rate
        self.fire_time += self.change_rate
        self.end_time += self.change_rate
        self.first = False
        self.sim(ax)

    def sub_fire_dealy(self, event):
        self.fire_delay -= self.change_rate
        self.fire_time -= self.change_rate
        self.end_time -= self.change_rate
        self.first = False
        self.sim(ax)

    def add_run_time(self, event):
        self.run_time += self.change_rate
        self.end_time += self.change_rate
        self.first = False
        self.sim(ax)

    def sub_run_time(self, event):
        self.run_time -= self.change_rate
        self.end_time -= self.change_rate
        self.first = False
        self.sim(ax)

    def update_acc(self, event):
        self.get_acc()
        self.first = False
        self.sim(ax)

    def get_acc(self):
        with open("acc_strg.json", "r") as file:
            self.acc_strategy = json.load(file)
        
    def sim(self, ax):
        self.spacecraft = Spacecraft(np.concatenate(([start_time], trajectory_data["earth"][start_time], [0])), trajectory_data)
        traj_history, vel_history, acc_history = run_sim(self.spacecraft, self.fire_time, self.fire_delay, self.end_time, self.init_vel, self.acc_strategy, self.trajectory_data)
        # print(self.fire_delay, self.run_time)
        if self.first == False:
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            zlim = ax.get_zlim()
        ax.cla()
        # solar.plot_trajectory(ax, traj_history, scale)
        # solar.plot_planet_trajectory(ax, trajectory_data, trajectory_data.keys(), self.spacecraft.time_list[self.fire_time], self.spacecraft.time_list[self.end_time], scale)
        if self.first == False:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            ax.set_zlim(zlim)
        return traj_history, vel_history, acc_history


dt = 3600
close_dt = 1
scale = 4e9
init_fire_delay = 242616
init_run_time = 175200
change_rate = 10000
trajectory_data = solar.get_trajectory()
conditions = Conditions(init_fire_delay, init_run_time, trajectory_data, change_rate)
start_time = list(trajectory_data["earth"].keys())[0]

ax = plt.subplot(projection='3d')
fire_delay, fire_time, end_time, init_vel = conditions.get_condition()
traj_history, vel_history, acc_history = conditions.sim(ax)
time = np.array(conditions.spacecraft.time_list[fire_time:end_time])

print(traj_history.shape, vel_history.shape, acc_history.shape, time.shape)
np.savez("spacecraft.npz", pos=traj_history, vel=vel_history, acc=acc_history, time=time)

ax_add_firedl = plt.axes([0.7, 0.09, 0.1, 0.06])  # [left, bottom, width, height] in figure coordinates
add_firedl = Button(ax_add_firedl, "Add DL")
add_firedl.on_clicked(conditions.add_fire_delay)

ax_sub_firedl = plt.axes([0.81, 0.09, 0.1, 0.06])
sub_firedl = Button(ax_sub_firedl, "Sub DL")
sub_firedl.on_clicked(conditions.sub_fire_dealy)

ax_add_runtime = plt.axes([0.7, 0.01, 0.1, 0.06])
add_runtime = Button(ax_add_runtime, "Add RT")
add_runtime.on_clicked(conditions.add_run_time)

ax_sub_runtime = plt.axes([0.81, 0.01, 0.1, 0.06])
sub_runtime = Button(ax_sub_runtime, "Sub RT")
sub_runtime.on_clicked(conditions.sub_run_time)

ax_acc_update = plt.axes([0.81, 0.17, 0.1, 0.06])
acc_update = Button(ax_acc_update, "acc")
acc_update.on_clicked(conditions.update_acc)

plt.legend()
# plt.show()