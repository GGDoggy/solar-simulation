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

def plot_planet_trajectory(ax, trajectories, planets, scale=0):
    for planet in planets:
        rs  = []
        for time in trajectories[planet]:
            rs.append(trajectories[planet][time])
        rs = np.array(rs)
        
        # ax.scatter(rs[:, 0], rs[:, 1], rs[:, 2], label=planet, s=0.1)
        ax.plot(rs[:, 0], rs[:, 1], rs[:, 2], label=planet)

    ax.scatter([0], [0], [0], color='yellow', label='sun')
    if scale != 0:
        rang = scale
        ax.axes.set_xlim3d(left=-rang, right=rang) 
        ax.axes.set_ylim3d(bottom=-rang, top=rang) 
        ax.axes.set_zlim3d(bottom=-rang, top=rang) 
        
def plot_trajectory(ax, trajectory, scale=0):
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], label="spacecraft")
    if scale != 0:
        rang = scale
        ax.axes.set_xlim3d(left=-rang, right=rang) 
        ax.axes.set_ylim3d(bottom=-rang, top=rang) 
        ax.axes.set_zlim3d(bottom=-rang, top=rang) 

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
    
    print(gene_state_table(get_trajectory()["mars"]))