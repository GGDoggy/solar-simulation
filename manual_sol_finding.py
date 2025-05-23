import numpy as np
import matplotlib.pyplot as plt
import solar
from simulation import Spacecraft

start_time = 2433283
end_time = 2457023
dt = 86400

trajectory_data = solar.get_trajectory()