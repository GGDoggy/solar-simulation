import matplotlib.pyplot as plt
import numpy as np

planets = [
    "earth",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune"
    ]

drop_ratio = 0

def plot_planet_trajectory(ax, trajectories, planets, start_time, end_time, scale=0):
    for planet in planets:
        rs  = []
        total_time = end_time - start_time
        for time in trajectories[planet]:
            if time > end_time:
                break
            if time > start_time + total_time * drop_ratio:
                rs.append(trajectories[planet][time])
        rs = np.array(rs)
        
        # ax.scatter(rs[:, 0], rs[:, 1], rs[:, 2], label=planet, s=0.1)
        ax.plot(rs[:, 0], rs[:, 1], rs[:, 2], label=planet)
        ax.scatter(rs[0, 0], rs[0, 1], rs[0, 2], c="green")
        ax.scatter(rs[-1, 0], rs[-1, 1], rs[-1, 2], c="red")

    ax.scatter([0], [0], [0], color='yellow', label='sun')
    if type(scale) == list:
        ax.axes.set_xlim3d(left=scale[0], right=scale[1]) 
        ax.axes.set_ylim3d(bottom=scale[2], top=scale[3]) 
        ax.axes.set_zlim3d(bottom=scale[4], top=scale[5])
    elif scale != 0:
        rang = scale
        ax.axes.set_xlim3d(left=-rang, right=rang) 
        ax.axes.set_ylim3d(bottom=-rang, top=rang) 
        ax.axes.set_zlim3d(bottom=-rang, top=rang)
        
def plot_trajectory(ax, trajectory, scale=0):
    start_plot = int(len(trajectory) * drop_ratio)
    ax.plot(trajectory[start_plot:-1, 0], trajectory[start_plot:-1, 1], trajectory[start_plot:-1, 2], label="spacecraft")
    if type(scale) == list:
        ax.axes.set_xlim3d(left=scale[0], right=scale[1]) 
        ax.axes.set_ylim3d(bottom=scale[2], top=scale[3]) 
        ax.axes.set_zlim3d(bottom=scale[4], top=scale[5])
    elif scale != 0:
        rang = scale
        ax.axes.set_xlim3d(left=-rang, right=rang) 
        ax.axes.set_ylim3d(bottom=-rang, top=rang) 
        ax.axes.set_zlim3d(bottom=-rang, top=rang)
    ax.scatter(trajectory[0, 0], trajectory[0, 1], trajectory[0, 2], c="orange")
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1], trajectory[-1, 2], c="red")

def gene_state_table(trajectories):
    ret = dict()
    for state in trajectories:
        add = np.delete(state, 0, 0)
        ret[state[0]] = add
    return ret

def get_trajectory():
    data = np.load("planet_trajectories.npz")
    ret = dict()
    for planet in data.keys():
        ret[planet] = gene_state_table(data[planet])
    return ret

if __name__ == "__main__":
    
    print(np.random.random())