import matplotlib.pyplot as plt
import math
import numpy as np
import itertools as it
import statistics as stat
from definitions import *

# all lengths are in meters
# all time in seconds
# all angles in radians if not specified otherwise
# all powers in dBW


#############################################################
#                       INITIALIZATION
#############################################################
wavelength = 2
dipole_spread = 1
antenna_spread = 15

frequency = SPEED_OF_LIGHT/wavelength

# reciever antenna x,y center
# dipoles1 = [
#     RxDipole(Position((-dipole_spread - antenna_spread) / 2, 0), Signal(0, 0, frequency)),
#     RxDipole(Position(( dipole_spread - antenna_spread) / 2, 0), Signal(0, 0, frequency))
# ]

# dipoles2 = [
#     RxDipole(Position((-dipole_spread + antenna_spread) / 2, 0), Signal(0, 0, frequency)),
#     RxDipole(Position(( dipole_spread + antenna_spread) / 2, 0), Signal(0, 0, frequency))
# ]

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
tx = TxDipole(Position(15, 20), Signal(phase=1, power=400, frequency=frequency))

# measured object x,y center
obj_position = Position(12, 30)


#############################################################
#                         SIMULATION
#############################################################
reflect=True
if reflect:
    object = TxDipole(obj_position, is_reflector=True)
    object.reflect_signal(tx)
else:
    object = TxDipole(obj_position, Signal(phase=1, power=400, frequency=frequency))


for antenna in antennas:
    for dipole in antenna.dipoles:
        # dipole.recieve_signal(tx)
        # dipole.recieve_signal(tx, reference=True)

        dipole.recieve_signal(object, phase_error_coef=0.00)


#############################################################
#                           PLOTS
#############################################################
# for i, antenna in enumerate(antennas):
#     print(f"{i + 1}. antenna-to-object angle = {calculate_deg_angle(antenna.dipoles[0].position, obj_position):.7f} deg.")

# for i, antenna in enumerate(antennas):
#     for j, dipole in enumerate(antenna.dipoles):
#         signal = dipole.get_normalized_signal()
#         print(f"{i + 1}. antenna, {j + 1}. dipole: phase={signal.phase:.7f} rsl={signal.power:.7f}")

target_position = detect_object_using_antenna_set_analytic(antennas, tx, obj_position, plot=True)
print(f"target position={target_position} found by analytic method")
target_position = detect_object_using_antenna_set_regression(antennas, tx, obj_position, plot=True)
print(f"target position={target_position} found by regression method")
target_position = detect_object_using_antenna_set_variance(antennas, tx, obj_position, plot=True)
print(f"target position={target_position} found by variance method")
