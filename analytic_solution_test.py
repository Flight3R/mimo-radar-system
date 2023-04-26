#%%

from definitions import *

# SPREAD
# spread > delta_wavelength
# to we can consider spread > wavelength safe
dipole_spread = 1
antenna_spread = 4
delta_wavelength = 0.5 #meters
wavelength = 1 #meters

frequency = SPEED_OF_LIGHT/wavelength

delta_phase = delta_wavelength / wavelength * 2 * math.pi
phase1, phase2 = [delta_phase, 0] if delta_phase > 0 else [0, delta_phase]

antennas = [
    RxAntennaArray([
        RxDipole(Position((-dipole_spread - antenna_spread) / 2, 0), Signal(phase1, 0, frequency)),
        RxDipole(Position(( dipole_spread - antenna_spread) / 2, 0), Signal(phase2, 0, frequency))
    ]),
    RxAntennaArray([
        RxDipole(Position((-dipole_spread + antenna_spread) / 2, 0), Signal(phase1, 0, frequency)),
        RxDipole(Position(( dipole_spread + antenna_spread) / 2, 0), Signal(phase2, 0, frequency))
    ])
]

fig, ax = plt.subplots()
ax.set_aspect(1)
for antenna in antennas:
    for dipole in antenna.dipoles:
        plot_antenna(ax, dipole, 'black')

regression_lines = []
for antenna in antennas:
    signal = antenna.dipoles[0].get_normalized_signal()
    delta_phase = wrap_phase(antenna.dipoles[0].signal.phase - antenna.dipoles[1].signal.phase)
    delta_wavelength = (delta_phase / (2 * math.pi)) * signal.getWavelangth()
    print(f"dipole_spread={dipole_spread}, delta_wavelength={delta_wavelength}")
    slope = math.sqrt(math.pow(dipole_spread / delta_wavelength, 2) - 1)
    regression_lines.append([slope, calculate_intercept(antenna.antenna_center, slope)])
    plot_regression_line(ax, antenna.antenna_center, -slope, 2)

crossing_point = calculate_crossing_of_lines(regression_lines[0], regression_lines[0])
plot_point(crossing_point)
