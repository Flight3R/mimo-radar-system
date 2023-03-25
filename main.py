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
wavelength = 2
dipole_spread = 1
antenna_spread = 10

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
tx = TxDipole(Position(15, 10), Signal(phase=0, power=400, frequency=frequency))

# measured object x,y center
obj_position = Position(7, 30)

phase_error_coef = 0.01
#############################################################
#                         SIMULATION
#############################################################
object = TxDipole(obj_position, is_reflector=True)

# simulate(antennas, tx, object, phase_error_coef)

#############################################################
#                           PLOTS
#############################################################
for output in glob.glob(f"{os.getcwd()}/*.png"):
    os.remove(output)

if True:
    method = [0, 1, 2]
    methods = [
        'analytic',
        'regression',
        'variance'
    ]
    for mt in method:
        end = time.time()
        target_position = detect_object_phase_increment(methods[mt], antennas, tx, object, phase_error_coef)
        start = time.time()
        print(f"target position={target_position} found by {methods[mt]} method,\t time={end-start}")
        print(f"target position error={calculate_distance(target_position, obj_position)}")
