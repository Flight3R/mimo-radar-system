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
wavelength = 2
dipole_spread = 1
antenna_spread = 8

frequency = SPEED_OF_LIGHT/wavelength
dipoles1 = [
    RxDipole(Position(-dipole_spread - antenna_spread / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position(               - antenna_spread / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position( dipole_spread - antenna_spread / 2, 0), Signal(0, 0, frequency))
]

dipoles2 = [
    RxDipole(Position(-dipole_spread + antenna_spread / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position(               + antenna_spread / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position( dipole_spread + antenna_spread / 2, 0), Signal(0, 0, frequency))
]


antennas = [
    RxAntennaArray(dipoles1),
    RxAntennaArray(dipoles2)
]


# transmitter antenna x,y center
tx = TxDipole(Position(10, 10), Signal(phase=0, power=100, frequency=frequency))

fig, ax = plt.subplots()
plot_scenario(ax, antennas, tx, None)
fig.savefig("scenario.png")

methods = [
    'analytic',
    'regression',
    'variance'
]

for method in methods:
    heat_map = create_heat_map(100, 0.25, method, antennas, tx, phase_error_coef=0.0, plot=True)
    # print(heat_map)
