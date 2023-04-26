#%%

from definitions import *
import numpy as np
# SPREAD
# spread > delta_wavelength
# to we can consider spread > wavelength safe
# if wavelength/spread gets smaller => resolution gets smaller
# so the best option is to set wavelength = spread
# print(f"antenna_spread; angle")
# for spread in np.linspace(1, 7, 50):
if True:
    spread = 1
    scale = 0.5
    wavelength = 1 #meters

    frequency = SPEED_OF_LIGHT/wavelength
    how_many_circles = 4

    delta_wavelength = scale * wavelength * 2 * math.pi
    phase1, phase2 = [delta_wavelength, 0] if delta_wavelength < 0 else [0, delta_wavelength]

    antenna = RxAntennaArray([
        RxDipole(Position(-spread/2, 0), Signal(phase1, 0 ,frequency)),
        RxDipole(Position( spread/2, 0), Signal(phase2, 0 ,frequency))
    ])

    fig, ax = plt.subplots()
    ax.set_aspect(1)
    angle = np.linspace(0, 2 * np.pi, 150)

    for dipole in antenna.dipoles:
        plot_antenna(ax, dipole, 'black')

    regression_lines = []
    figure_centers = []
    for i in range(how_many_circles):
        circles = []
        for dipole in antenna.dipoles:
            signal = dipole.get_normalized_signal()
            radius = (signal.phase / (2 * math.pi)) * signal.getWavelangth() + (i + 1)  * signal.getWavelangth()
            x =  radius * np.cos(angle) + dipole.position.x
            y =  radius * np.sin(angle) + dipole.position.y
            ax.plot(x, y, color='gray')
            circles.append([dipole.position.x, dipole.position.y, radius])

        cross_points_of_circles = []
        for pair in generate_pairs(circles):
            intersections = get_intersections(pair)
            if intersections is not None:
                x0, y0, x1, y1 = intersections
                if y0 > 0:
                    point = Position(x0, y0)
                else:
                    point = Position(x1, y1)
                cross_points_of_circles.append(point)
                plot_point(ax, point, marker='.')
        if len(cross_points_of_circles) > 0:
            figure_center = calculate_figure_center(cross_points_of_circles)
            figure_centers.append(figure_center)
    slope, intercept = calculate_linear_regression(figure_centers)
    plot_regression_line(ax, Position(0,0), slope, length=10)
    print(f"alpha = {90 - abs(math.atan(slope) * 360 / (2 * math.pi))}")
    # print(f"{spread}; {90 - abs(math.atan(slope) * 360 / (2 * math.pi))}")