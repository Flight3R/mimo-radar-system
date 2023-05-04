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


for output in glob.glob(f"{os.getcwd()}/*.csv") + glob.glob(f"{os.getcwd()}/*.png"):
    os.remove(output)

with open("pos_err_normal.csv", "a") as myfile:
    myfile.write("rng_run;method;phase_err;pos_err\n")
with open("pos_err_phinc.csv", "a") as myfile:
    myfile.write("rng_run;method;phase_err;pos_err\n")


for rng_run in range(200, 210):
    random.seed(rng_run)
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

        methods = [
            'analytic',
            'regression',
            'variance'
        ]

        if True:
            for method in methods:
                detection_method = select_detection_method(method)
                target_position = detection_method(antennas, tx, obj_position, plot=False)
                pos_err = calculate_distance(target_position, obj_position)
                # if pos_err is not None:
                with open("pos_err_normal.csv", "a") as myfile:
                    myfile.write(f"{rng_run};{method};{phase_err};{pos_err}\n")

        if True:
            for method in methods:
                target_position = detect_object_phase_increment(method, antennas, tx, object, phase_error_coef, plot=False)
                pos_err = calculate_distance(target_position, obj_position)
                # if pos_err is not None:
                with open("pos_err_phinc.csv", "a") as myfile:
                    myfile.write(f"{rng_run};{method};{phase_err};{pos_err}\n")
