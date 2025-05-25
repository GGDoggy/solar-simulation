import numpy as np
import matplotlib.pyplot as plt
import json
import solar

data = np.load("spacecraft.npz")
pos_data = data["pos"]
vel_data = data["vel"]
acc_data = data["acc"]
times = data["time"]

radi = []
ang = []
z = []
v_r = []
v_the = []
v_z = []
a_vel = []
a_2 = []
a_z = []
ang_mom = []
revo = 0
last_ang = 0
for i, time in enumerate(times):
    pos = pos_data[i]
    vel = vel_data[i]
    acc = acc_data[i]

    n_z = np.array([0, 0, 1])
    r = pos.copy()
    r[2] = 0
    r_norm = np.linalg.norm(r)
    n_r = r / r_norm
    n_the = np.cross(n_z, n_r)

    rot = np.linalg.inv(np.concatenate((n_r, n_the, n_z)).reshape(3, 3).T)
    vel_tran = np.matmul(rot, vel)

    v = vel.copy()
    v[2] = 0
    n_v = v / np.linalg.norm(v)
    n_2 = np.cross(n_z, n_v)

    rot = np.linalg.inv(np.concatenate((n_v, n_2, n_z)).reshape(3, 3).T)
    acc_tran = np.matmul(rot, acc)

    raw_ang = np.arctan(r[1] / r[0]) + revo * np.pi + np.pi / 2
    if raw_ang < last_ang:
        raw_ang += np.pi
        revo += 1
    last_ang = raw_ang

    radi.append(r_norm)
    ang.append(raw_ang)
    z.append(pos[2])
    v_r.append(vel_tran[0])
    v_the.append(vel_tran[1])
    v_z.append(vel_tran[2])
    a_vel.append(acc_tran[0])
    a_2.append(acc_tran[1])
    a_z.append(acc_tran[2])
    ang_mom.append(np.linalg.norm(np.cross(pos, vel)))

radi = np.array(radi)
ang = np.array(ang)
z = np.array(z)
v_r = np.array(v_r) 
v_the = np.array(v_the)
v_z = np.array(v_z)
a_vel = np.array(a_vel)
a_2 = np.array(a_2)
a_z = np.array(a_z)
ang_mom = np.array(ang_mom)

# fig, axs = plt.subplots(3)
# fig.subplots_adjust(hspace=0.6)
# fig.suptitle('Position vs. Time')
# axs[0].plot(times, radi)
# axs[1].plot(times, ang)
# axs[2].plot(times, z)
# axs[0].set_title('Radial Position')
# axs[1].set_title('Angular Position')
# axs[2].set_title('Vertical Position')
# axs[2].set_xlabel('Time (s)')

# fig, axs = plt.subplots(3)
# fig.subplots_adjust(hspace=0.6)
# fig.suptitle('Velocity vs. Time')
# axs[0].plot(times, v_r)
# axs[1].plot(times, v_the)
# axs[2].plot(times, v_z)
# axs[0].set_title('Radial Velocity')
# axs[1].set_title('Tangential Velocity')
# axs[2].set_title('Vertical Velocity')
# axs[2].set_xlabel('Time (s)')

# fig, axs = plt.subplots(3)
# fig.subplots_adjust(hspace=0.6)
# fig.suptitle('Boost Acceleration vs. Time')
# axs[0].plot(times, a_vel)
# axs[1].plot(times, a_2)
# axs[2].plot(times, a_z)
# axs[0].set_title('Forward Acceleration')
# axs[1].set_title('Side Acceleration')
# axs[2].set_title('Vertical Acceleration')
# axs[2].set_xlabel('Time (s)')

# fig, ax = plt.subplots()
# ax.plot(times, ang_mom)
# ax.set_title('Angular Momentum vs. Time')

# fig, ax = plt.subplots()
# ax.plot(ang, radi)
# ax.set_title('Radial Position vs. Angular Position')

ax = plt.subplot(projection='3d')
solar.plot_trajectory(ax, pos_data, 5e9)
solar.plot_planet_trajectory(ax, solar.get_trajectory(), ["earth", "mars", "jupiter", "saturn", "uranus", "neptune"], times[0], times[-1], 5e9)

plt.show()