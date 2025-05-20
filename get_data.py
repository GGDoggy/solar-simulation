import requests
import urllib.parse
import numpy as np

planets = [
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune"
]
para_exam = {
    'format':"text",
    # 'COMMAND':"'mars bary'",
    'OBJ_DATA':"'YES'",
    'MAKE_EPHEM':"'YES'",
    'EPHEM_TYPE':"'VECTORS'",
    'CENTER':"'@sun'",
    'REF_PLANE':"'ECLIPTIC'",
    'QUANTITIES':"'1'"
}

def send_request(planet, start_time, stop_time, time_span):
    start_time = "JD" + str(start_time)
    stop_time = "JD" + str(stop_time)
    para = para_exam.copy()
    para['START_TIME'] = start_time
    para['STOP_TIME'] = stop_time
    para['STEP_SIZE'] = time_span
    if planet != "earth":
        para.update({'COMMAND': f"'{planet} bary'"})
        url_para = urllib.parse.urlencode(para)
        print(url_para)

        req = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api?" + url_para)
        with open(f"{planet}.get.txt", "w", encoding="utf-8") as file:
            file.write(req.content.decode("utf-8"))
        
    else:
        para.update({"COMMAND": "sun"})
        para.pop("CENTER")
        url_para = urllib.parse.urlencode(para)
        print(url_para)
        req = requests.get("https://ssd.jpl.nasa.gov/api/horizons.api?" + url_para)
        with open("sun_from_earth.get.txt", "w", encoding="utf-8") as file:
            file.write(req.content.decode("utf-8"))

def get_trajectory(planet, start_day, end_day):
    res = np.zeros((1, 7), dtype=np.longdouble)
    send_request(planet, start_day, end_day, "1d")

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

    for i, line in enumerate(lines):
        if i % 4 == 0:  # state: (time, x, y, z, vx, vy, vz)
            state = np.zeros(7, dtype=np.longdouble)
            state[0] = np.longdouble(line.split()[0])
        if i % 4 == 1:
            r_data = line.strip().split("=")[1:]
            state[1] = np.longdouble(r_data[0].split()[0]) * earth_inv
            state[2] = np.longdouble(r_data[1].split()[0]) * earth_inv
            state[3] = np.longdouble(r_data[2]) * earth_inv
        if i % 4 == 2:
            v_data = line.strip().split("=")[1:]
            state[4] = np.longdouble(v_data[0].split()[0]) * earth_inv
            state[5] = np.longdouble(v_data[1].split()[0]) * earth_inv
            state[6] = np.longdouble(v_data[2]) * earth_inv
            state = state.reshape((1, 7))
            res = np.concatenate((res, state), dtype=np.longdouble)
    return np.delete(res, 0, 0)

def get_all_traj(planet, start_day, end_day):
    get_range = 3750
    res = np.zeros((1, 7), dtype=np.longdouble)
    for i in range(int((end_day - start_day) / get_range)):
        res = np.concatenate((res, get_trajectory(planet, start_day + get_range * i, start_day + get_range * (i+1))), dtype=np.longdouble)
    res = np.concatenate((res, get_trajectory(planet, start_day + get_range * int((end_day - start_day) / get_range), end_day)), dtype=np.longdouble)
    s0 = 0
    dele = []
    for i, s in enumerate(res):
        if s0 == s[0]:
            dele.append(i)
        s0 = s[0]
    return np.delete(res, dele, 0)

start_day = 2433283
end_day = 2457023

np.savez("planet_trajectories.npz",
    mars=get_all_traj("mars", start_day, end_day),
    jupiter=get_all_traj("jupiter", start_day, end_day),
    saturn=get_all_traj("saturn", start_day, end_day),
    uranus=get_all_traj("uranus", start_day, end_day),
    neptune=get_all_traj("neptune", start_day, end_day),
    earth=get_all_traj("earth", start_day, end_day),
)