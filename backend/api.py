import glob
import os
import time

from definitions import *

def create_antenna_array(dipole_number: int, dipole_spread: int, wavelength: float,
                         center_position: Position) -> RxAntennaArray:
    dipoles = []
    frequency = SPEED_OF_LIGHT / wavelength
    center_x, center_y = center_position.x, center_position.y
    min_x = center_x - ((dipole_number - 1) * dipole_spread) / 2
    max_x = center_x + ((dipole_number - 1) * dipole_spread) / 2
    for x in np.linspace(min_x, max_x, dipole_number):
        print(x)
        dipoles.append(RxDipole(Position(x, center_y), Signal(0, 0, frequency)))
    return RxAntennaArray(dipoles)


def create_transmitter(positon: Position, phase_offset: float, wavelength: float) -> TxDipole:
    frequency = SPEED_OF_LIGHT / wavelength
    return TxDipole(positon, Signal(phase=phase_offset, power=0, frequency=frequency))


def create_object(positon: Position) -> TxDipole:
    return TxDipole(positon, is_reflector=True)


# all lengths are in meters
# all time in seconds
# all angles in radians if not specified otherwise
# all powers in dBW

#############################################################
#                       INITIALIZATION
#############################################################
wavelength = 2 #todo dodać do wprowadzania
dipole_spread = 1
antenna_spread = 15

frequency = SPEED_OF_LIGHT / wavelength
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
tx = TxDipole(Position(15, 10), Signal(phase=1, power=400, frequency=frequency))

# measured object x,y center
obj_position = Position(5, -30)

phase_error_coef = 0.00
#############################################################
#                         SIMULATION
#############################################################
object = TxDipole(obj_position, is_reflector=True)

simulate(antennas, tx, object, phase_error_coef)

#############################################################
#                           PLOTS
#############################################################
for output in glob.glob(f"{os.getcwd()}/*.png"):
    os.remove(output)

method = [0, 1, 2]
methods = [
    'analytic',
    'regression',
    'variance'
]

if True:
    for mt in method:
        detection_method = select_detection_method(methods[mt])
        start = time.time()
        target_position = detection_method(antennas, tx, obj_position, plot=True)
        end = time.time()
        print(f"{' OBJECT DETECTION ' :=^50}")
        print(f"{'method=': <20}{methods[mt]}")
        if target_position is not None:
            print(f"{'target_position=' : <20}{target_position :.5}")
            print(f"{'position error=' : <20}{calculate_distance(target_position, obj_position) :.5}")
        else:
            print(f"{'target_position=' : <20}{'Not found'}")
        print(f"{'time=' : <20}{end - start :.5}")

if True:
    for mt in method:
        start = time.time()
        target_position = detect_object_phase_increment(methods[mt], antennas, tx, object, phase_error_coef, plot=True)
        end = time.time()
        print(f"{' OBJECT DETECTION - phase increment ' :=^50}")
        print(f"{'method=': <20}{methods[mt]}")
        if target_position is not None:
            print(f"{'target_position=' : <20}{target_position :.5}")
            print(f"{'position error=' : <20}{calculate_distance(target_position, obj_position) :.5}")
        else:
            print(f"{'target_position=' : <20}{'Not found'}")
        print(f"{'time=' : <20}{end - start :.5}")


def detect_object(method: str, phase_increment: bool, antennas: list, tx: TxDipole, object: TxDipole, phase_error_coef=0.0) -> Position:
    if phase_increment:
        return detect_object_phase_increment(method, antennas, tx, object, phase_error_coef)
    else:
        simulate(antennas, tx, object, phase_error_coef)
        detection_method = select_detection_method(method)
        return detection_method(antennas, tx, object.position)