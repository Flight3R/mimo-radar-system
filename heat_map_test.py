#%%
from definitions import *
import os
import glob
import time

# edge_length = 50
# x_space = np.linspace(-50, 50, edge_length)
# y_space = np.linspace(-50, 50, edge_length)
# heat_map = np.ones((edge_length, edge_length))
# heat_map[edge_length-5:edge_length, edge_length-5:edge_length] = np.zeros((5, 5))
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# ax.pcolormesh(x_space, y_space, heat_map)


#############################################################
#                       INITIALIZATION
#############################################################
dipole_number = 3
dipole_spread = 1
wavelength = 2

antennas = [
    create_antenna_array(dipole_number, dipole_spread, wavelength, center_position=Position(-10.0, 0.0)),
    create_antenna_array(dipole_number, dipole_spread, wavelength, center_position=Position(10.0, 0.0))
]
# transmitter antenna x,y center
tx = TxDipole(Position(15, 10), Signal(phase=0, power=1, frequency=SPEED_OF_LIGHT/wavelength))

# fig, ax = plt.subplots()
# plot_scenario(ax, antennas, tx, None)
# fig.savefig("plots&data/scenario.png")

methods = [
    'analytic',
    'regression',
    'variance'
]

edge_length = 100
resolution = math.sqrt(512 / (edge_length ** 2))

for method in methods:
    heat_map = create_heat_map(edge_length, resolution, method, antennas, tx, phase_error_coef=0.0, plot=True)
    # print(heat_map)
