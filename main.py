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
antenna_spread = 15

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
tx = TxDipole(Position(15, 10), Signal(phase=3, power=400, frequency=frequency))

# measured object x,y center
obj_position = Position(5, -30)

with open("pos_err.csv", "a") as myfile:
    myfile.write("rng_run; method; phase_err; pos_err\n")

for rng_run in range(5):
    for phase_err in np.linspace(0.001, 0.06, 100):

        phase_error_coef = phase_err
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
                target_position = detection_method(antennas, tx, obj_position, plot=False)
                if target_position is not None:
                    with open("pos_err.csv", "a") as myfile:
                        myfile.write(f"{rng_run}; {methods[mt]}; {phase_err}; {calculate_distance(target_position, obj_position)}\n")

        # if True:
        #     for mt in method:
        #         start = time.time()
        #         target_position = detect_object_phase_increment(methods[mt], antennas, tx, object, phase_error_coef, plot=False)
        #         end = time.time()
        #         # print(f"{' OBJECT DETECTION - phase increment ' :=^50}")
        #         # print(f"{'method=': <20}{methods[mt]}")
        #         # if target_position is not None:
        #         #     print(f"{'target_position=' : <20}{target_position :.5}")
        #         #     print(f"{'position error=' : <20}{calculate_distance(target_position, obj_position) :.5}")
        #         # else:
        #         #     print(f"{'target_position=' : <20}{'Not found'}")
        #         # print(f"{'time=' : <20}{end-start :.5}")
