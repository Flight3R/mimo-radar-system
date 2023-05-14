from definitions import *
import os
import glob
import time

# all lengths are in meters
# all time in seconds
# all angles in radians if not specified otherwise
# all powers in dBW

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
tx = TxDipole(Position(-15, 10), Signal(phase=0, power=1, frequency=SPEED_OF_LIGHT/wavelength))

# measured object x,y center
obj_position = Position(3, 20)

phase_error_coef = 0.0
#############################################################
#                         SIMULATION
#############################################################
object = TxDipole(obj_position, is_reflector=True)

simulate(antennas, tx, object, phase_error_coef)

#############################################################
#                           PLOTS
#############################################################


fig, ax = plt.subplots()
plot_scenario(ax, antennas, tx, obj_position)
pos = detect_object('variance', True, antennas, tx, object, phase_error_coef)
plot_point(ax, pos)
print(f'{pos.x}, {pos.y}')
plt.savefig('scenario.png')