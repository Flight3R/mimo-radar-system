import matplotlib.pyplot as plt
import math
import numpy as np
import itertools as it
import statistics as stat
import random


SPEED_OF_LIGHT = 299792458


#############################################################
#                         FUNCTIONS
#############################################################
def calculate_crossing_of_lines(line_parameters1, line_parameters2):
    slope1, intercept1 = line_parameters1
    slope2, intercept2 = line_parameters2
    x = (intercept1 - intercept2) / (slope2 - slope1)
    y = slope1 * x + intercept1
    return Position(x, y)


def calculate_linear_regression(positions):
    array_x = [position.x for position in positions]
    array_y = [position.y for position in positions]
    slope, intercept = stat.linear_regression(array_x, array_y)
    return slope, intercept


def calculate_intercept(point, slope):
    return point.y - slope * point.x


def calculate_figure_center(positions):
    mean_x = stat.mean([position.x for position in positions])
    mean_y = stat.mean([position.y for position in positions])
    return Position(mean_x, mean_y)


def calculate_figure_center_variance(positions):
    variance_x = stat.variance([position.x for position in positions])
    variance_y = stat.variance([position.y for position in positions])
    return stat.mean([variance_x, variance_y])


def calculate_line(point_A, point_B):
    slope = (point_A.y - point_B.y) / (point_A.x - point_B.x)
    intercept = calculate_intercept(point_A, slope)
    return [slope, intercept]


def calculate_deg_angle(position1, position2):
    slope, _ = calculate_line(position1, position2)
    return slope * 360 / (2 * math.pi)


def calculate_phase(frequency, theha_zero, distance):
    wavelength = SPEED_OF_LIGHT / frequency
    return wrap_phase(theha_zero + (distance / wavelength) % 1 * 2 * math.pi)


def calculate_fsl(distance, frequency):
    return 32.44 + 20 * math.log10(distance) + 20 * math.log10(frequency / 1e6)


def calculate_distance(position1, position2):
    return math.sqrt(math.pow(position1.x - position2.x, 2)
                        + math.pow(position1.y - position2.y, 2))


def generate_pairs(array):
    return list(it.combinations(array, 2))


def get_intersections(pair):
    x0, y0, r0 = pair[0]
    x1, y1, r1 = pair[1]

    d=math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0 - r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a = (math.pow(r0, 2) - math.pow(r1, 2) + math.pow(d, 2)) / (2 * d)
        h = math.sqrt(math.pow(r0, 2) - math.pow(a, 2))
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d
        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d
        return x3, y3, x4, y4


def plot_point(ax, position, color='blue', marker='o'):
    ax.plot(position.x, position.y, color=color, marker=marker, )


def plot_antenna(ax, antenna, color):
    ax.plot(antenna.position.x, antenna.position.y, color=color, marker='o')


def plot_line_between(ax, position1, position2, color):
    ax.plot([position1.x, position2.x], [position1.y, position2.y], color=color)


def plot_regression_line(ax, start_point, slope, length):
    d_y = math.sqrt(math.pow(length, 2)
                        * math.pow(slope, 2) / (1 + math.pow(slope, 2)))
    y1 = start_point.y + d_y

    intercept = calculate_intercept(start_point, slope)
    x = lambda y: (y - intercept) / slope
    x1 = x(y1)

    end_point = Position(x1, y1)
    plot_line_between(ax, start_point, end_point, 'purple')


def plot_scenario(ax, antennas, tx, obj_position):
    plot_antenna(ax, tx, 'green')
    plot_line_between(ax, tx.position, obj_position, 'yellow')
    for antenna in antennas:
        for dipole in antenna.dipoles:
            plot_antenna(ax, dipole, 'black')
            plot_line_between(ax, dipole.position, obj_position, 'yellow')


def connect_antennas(antenna1, antenna2):
    plot_line_between([antenna1.x, antenna1.y], [antenna2.x, antenna2.y])


def wrap_phase(phase):
    return phase % (2 * math.pi)


def detect_object_using_antenna_set_variance(antennas, tx=None, obj_position=None, plot=False):
    if plot:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plot_scenario(ax, antennas, tx, obj_position)
    target_position = None
    angle = np.linspace(0, 2 * np.pi, 150)
    how_many_circles = 20
    for antenna in antennas:
        previous_variance = math.inf
        previous_center = None
        figure_centers = []
        for i in range(how_many_circles):
            circles = []
            for dipole in antenna.dipoles:
                signal = dipole.get_normalized_signal()
                delta_wavelength = (signal.phase /
                                        (2 * math.pi)) * signal.getWavelangth()
                radius = delta_wavelength + (i + 1)  * signal.getWavelangth()
                circles.append([dipole.position.x, dipole.position.y, radius])
                if plot:
                    x =  radius * np.cos(angle) + dipole.position.x
                    y =  radius * np.sin(angle) + dipole.position.y
                    ax.plot(x, y, color='gray')

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
                    if plot:
                        plot_point(ax, point, marker='.')

            if len(cross_points_of_circles) > 0:
                figure_center = calculate_figure_center(cross_points_of_circles)
                figure_centers.append(figure_center)

            # try to calculate position of object basing on changing variance
            if len(cross_points_of_circles) > 1:
                current_variance = calculate_figure_center_variance(cross_points_of_circles)
                if current_variance > previous_variance:
                    target_position = previous_center
                    break
                else:
                    previous_variance = current_variance
                    previous_center = figure_center

    if plot and target_position is not None:
        plot_point(ax, target_position, 'magenta', '*')
        plt.savefig('radar_output_variance.png')

    return target_position


def detect_object_using_antenna_set_analytic(antennas, tx=None, obj_position=None, plot=False):
    if plot:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plot_scenario(ax, antennas, tx, obj_position)
    regression_lines_analytic = []
    for antenna in antennas:
        delta_phase = wrap_phase(antenna.dipoles[0].signal.phase
                                    - antenna.dipoles[-1].signal.phase)
        delta_wavelength = delta_phase / (2 * math.pi) * antenna.dipoles[0].signal.getWavelangth()
        slope = math.sqrt(math.pow(antenna.antenna_diameter
                                      / delta_wavelength, 2) - 1)
        regression_lines_analytic.append([slope,
                                          calculate_intercept(antenna.antenna_center,
                                                              slope)])
        if plot:
            plot_regression_line(ax, antenna.antenna_center, slope, 20)

    # calculate position of object basing on analytic solution
    line_parameters1, line_parameters2 = regression_lines_analytic
    target_position = calculate_crossing_of_lines(line_parameters1,
                                                  line_parameters2)
    if plot:
        plot_point(ax, target_position, 'magenta', '*')
        plt.savefig('radar_output_analytic.png')
    return target_position


def detect_object_using_antenna_set_regression(antennas, tx=None, obj_position=None, plot=False):
    if plot:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        plot_scenario(ax, antennas, tx, obj_position)
    angle = np.linspace(0, 2 * np.pi, 150)
    how_many_circles = 20
    regression_lines = []
    for antenna in antennas:
        cross_points_of_circles = []
        for i in range(how_many_circles):
            circles = []
            for dipole in antenna.dipoles:
                signal = dipole.get_normalized_signal()
                delta_wavelength = (signal.phase / (2 * math.pi)) * signal.getWavelangth()
                radius = delta_wavelength + (i + 1)  * signal.getWavelangth()
                circles.append([dipole.position.x, dipole.position.y, radius])
                if plot:
                    x =  radius * np.cos(angle) + dipole.position.x
                    y =  radius * np.sin(angle) + dipole.position.y
                    ax.plot(x, y, color='gray')

            for pair in generate_pairs(circles):
                intersections = get_intersections(pair)
                if intersections is not None:
                    x0, y0, x1, y1 = intersections
                    if y0 > 0:
                        point = Position(x0, y0)
                    else:
                        point = Position(x1, y1)
                    cross_points_of_circles.append(point)
                    if plot:
                        plot_point(ax, point, marker='.')

        slope, intercept = calculate_linear_regression(cross_points_of_circles)
        regression_lines.append([slope, intercept])

    # calculate position of object basing on linear regressions
    line_parameters1, line_parameters2 = regression_lines
    target_position = calculate_crossing_of_lines(line_parameters1, line_parameters2)
    if plot:
        plot_point(ax, target_position, 'magenta', '*')
        plt.savefig('radar_output_regression.png')
    return target_position


#############################################################
#                          CLASSES
#############################################################
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def move(self, target_position, speed, delta_time):
        slope, _ = calculate_line(self, target_position)
        delta_distance = speed * delta_time
        delta_x = math.sqrt(math.pow(delta_distance, 2)
                                / (1 + math.pow(slope, 2)))
        moving_left = target_position.x < self.x
        delta_x = -delta_x if moving_left else delta_x
        delta_y = slope * delta_x
        self.x += delta_x
        self.y += delta_y


class Signal():
    def __init__(self, phase, power, frequency):
        self.phase = wrap_phase(phase)
        self.power = power
        self.frequency = frequency

    def getWavelangth(self):
        return SPEED_OF_LIGHT/self.frequency

    def setPhase(self, phase):
        self.phase = wrap_phase(phase)


class Dipole:
    def __init__(self, position, signal):
        self.position = position
        self.signal = signal


class TxDipole(Dipole):
    def __init__(self, position, signal=Signal(0,0,0), is_reflector=False):
        super().__init__(position, signal)
        self.is_reflector = is_reflector

        if(is_reflector):
            self.signal = Signal(0, 0, 0)

    def reflect_signal(self, txAnt):
        distance = calculate_distance(self.position, txAnt.position)
        fsl = calculate_fsl(distance, txAnt.signal.frequency)
        rsl = txAnt.signal.power - fsl
        if (rsl > 0):
            phase = calculate_phase(txAnt.signal.frequency,
                                    txAnt.signal.phase,
                                    distance)
            self.signal = Signal(phase, rsl, txAnt.signal.frequency)
        else:
            print("reflected signal power = 0!")


class RxDipole(Dipole):
    def __init__(self, position, signal):
        super().__init__(position, signal)
        self.signal = signal
        self.reference_signal = Signal(0, 0, 0)

    def recieve_signal(self, txAnt, reference=False, phase_error_coef=0):
        if (txAnt.signal.power > 0):
            distance = calculate_distance(self.position, txAnt.position)
            current_fsl = calculate_fsl(distance, txAnt.signal.frequency)
            current_rsl = txAnt.signal.power - current_fsl
            phase_error = random.uniform(-2 * math.pi, 2 * math.pi) * phase_error_coef
            if (reference):
                if (current_rsl > 0):
                    self.reference_signal.setPhase(
                        calculate_phase(txAnt.signal.frequency,
                                        txAnt.signal.phase,
                                        distance) + phase_error)
                    self.reference_signal.power = current_rsl
                    self.reference_signal.frequency = txAnt.signal.frequency
                else:
                    print("reference signal RSL=0!")
            else:
                if (current_rsl > 0):
                    self.signal.setPhase(self.signal.phase +
                                         calculate_phase(txAnt.signal.frequency, txAnt.signal.phase, distance) *
                                            current_rsl / (current_rsl + self.signal.power)
                                         + phase_error)
                    self.signal.power += current_rsl
                else:
                    print("RSL=0")

    def get_normalized_signal(self):
        if self.reference_signal.power > 0 and self.signal.power != self.reference_signal.power:
            phase = (self.signal.phase * self.signal.power
                        - self.reference_signal.phase * self.reference_signal.power) / (self.signal.power - self.reference_signal.power)
            power = self.signal.power - self.reference_signal.power
            return Signal(phase, power, self.signal.frequency)
        else:
            return self.signal


class RxAntennaArray:
    def __init__(self, dipoles):
        self.antenna_diameter = abs(dipoles[0].position.x - dipoles[-1].position.x)
        self.dipoles = dipoles
        self.antenna_center = calculate_figure_center([dipole.position for dipole in dipoles])
