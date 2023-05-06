#%%
from definitions import *
import os
import glob
import time

wavelength = 3

frequency = SPEED_OF_LIGHT/wavelength

antena1 = create_antenna_array(dipole_number=3, dipole_spread=wavelength, wavelength=wavelength, center_position=Position(-10, -2))
antena2 = create_antenna_array(dipole_number=3, dipole_spread=wavelength, wavelength=wavelength, center_position=Position(2, 2))
antennas = [antena1, antena2]

phase_offset = np.linspace(0, 2*np.pi, 10)
for po in phase_offset:
    tx = TxDipole(Position(15, 10), Signal(phase=po, power=400, frequency=frequency))
    object = TxDipole(Position(0, 30), is_reflector=True)

    simulate(antennas, tx, object)
    pos = detect_object_using_antenna_set_regression(antennas, tx, object.position, plot=True)

    if pos is not None:
        print(f"FOUND, {po=}")
        break

fig, ax = plt.subplots()
plot_scenario(ax, antennas, tx, object.position)
fig.savefig('plots&data/scenario.png')
