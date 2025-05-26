import numpy as np
import scipy.io as io

# io.savemat("planet_trajectories.mat", mdict=np.load("planet_trajectories.npz"))
io.savemat("spacecraft.mat", mdict=np.load("spacecraft.npz"))
# vo2 = np.load("voyager2.npz")
# print(vo2["voyager2"].shape)
# io.savemat("voyager2.mat", mdict=vo2)