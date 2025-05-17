import matplotlib.pyplot as plt
import numpy as np

def get_trajectory(planets):
    trajectories = dict()
    for planet in planets:
        if planet == "earth":
            with open("sun_from_earth.get.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = lines[lines.index("$$SOE\n") + 1: lines.index("$$EOE\n")]
                earth_inv = -1
        else:
            with open(f"{planet}.get.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = lines[lines.index("$$SOE\n") + 1: lines.index("$$EOE\n")]
                earth_inv = 1

        rs = []
        for i, line in enumerate(lines):
            if i % 4 == 1:
                line = line.strip().split("=")
                x = float(line[1].strip().split()[0])
                y = float(line[2].strip().split()[0])
                z = float(line[3].strip())
                r = np.array([x, y, z])
                rs.append(r * earth_inv)
        
        trajectories[planet] = np.array(rs)
    return trajectories

def get_init_condition(planets):
    init = dict()
    for planet in planets:
        if planet == "earth":
            with open("sun_from_earth.get.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = lines[lines.index("$$SOE\n") + 1: lines.index("$$EOE\n")]
                earth_inv = -1
        else:
            with open(f"{planet}.get.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = lines[lines.index("$$SOE\n") + 1: lines.index("$$EOE\n")]
                earth_inv = 1
                
        v_data = lines[2].strip().split("=")[1:]
        x = float(v_data[0].split()[0])
        y = float(v_data[1].split()[0])
        z = float(v_data[2])
        vel = np.array([x, y, z]) * earth_inv
        r_data = lines[1].strip().split("=")[1:]
        x = float(r_data[0].split()[0])
        y = float(r_data[1].split()[0])
        z = float(r_data[2])
        pos = np.array([x, y, z]) * earth_inv
        # {'planet': [[x, y, z], [vx, vy, vz]]}
        init[planet] = [pos, vel]
    return init

def plot_trajectory(trajectories, planets, scale=0):
    ax = plt.subplot(projection='3d')

    for planet in planets:
        rs = trajectories[planet]
        # ax.scatter(rs[:, 0], rs[:, 1], rs[:, 2], label=planet, s=0.1)
        ax.plot(rs[:, 0], rs[:, 1], rs[:, 2], label=planet)

    ax.scatter([0], [0], [0], color='yellow', label='Sun')
    if scale != 0:
        rang = scale
        ax.axes.set_xlim3d(left=-rang, right=rang) 
        ax.axes.set_ylim3d(bottom=-rang, top=rang) 
        ax.axes.set_zlim3d(bottom=-rang, top=rang) 
    

if __name__ == "__main__":
    planets = [
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "earth"
    ]

    trajectories = get_trajectory(planets)
    plot_trajectory(trajectories, planets, 5e9)
    plt.show()