# %%
import matplotlib.pyplot as plt
import math
import numpy as np
import itertools as it
import statistics as stat


# all lengths are in meters
# all time in seconds
# all angles in radians if not specified otherwise
# all powers in dB


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


def linear_regression(positions):
    array_x = [position.x for position in positions]
    array_y = [position.y for position in positions]
    slope, intercept = stat.linear_regression(array_x, array_y)
    return slope, intercept

def plot_regression_line(ax, x0, slope, intercept, length):
    x1 = x0 + (length/np.sqrt(1+slope**2))
    x2 = x0 - (length/np.sqrt(1+slope**2))

    f = lambda x: slope * x + intercept
    y0 = f(x0)
    y1 = f(x1)
    y2 = f(x2)

    x, y = [x1, y1] if y1 > 0 else [x2, y2]
    start_point = Position(x0, y0)
    end_point = Position(x, y)
    plot_line_between(ax, start_point, end_point, 'purple')


def calculate_figure_center(positions):
    mean_x = stat.mean([position.x for position in positions])
    mean_y = stat.mean([position.y for position in positions])
    return Position(mean_x, mean_y)


def calculate_figure_center_variance(positions):
    variance_x = stat.variance([position.x for position in positions])
    variance_y = stat.variance([position.y for position in positions])
    return stat.mean([variance_x, variance_y])

def calculate_angle(position1, position2):
    rx = position1.x - position2.x
    ry = position1.y - position2.y
    # angle in degrees
    return math.atan(rx / ry) * 360 / (2 * math.pi)


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


def connect_antennas(antenna1, antenna2):
    plot_line_between([antenna1.x, antenna1.y], [antenna2.x, antenna2.y])


def plot_line_between(ax, position1, position2, color):
    ax.plot([position1.x, position2.x], [position1.y, position2.y], color=color)


def wrap_phase(phase):
    return phase % (2 * math.pi)


def calculate_phase(frequency, theha_zero, distance):
    wavelength = SPEED_OF_LIGHT / frequency
    return wrap_phase(theha_zero + (distance % wavelength) / wavelength * 2 * math.pi)


def calculate_fsl(distance, frequency):
    return 32.44 + 20 * math.log10(distance) + 20 * math.log10(frequency / 1e6)


def calculate_distance(position1, position2):
    return math.sqrt(math.pow(position1.x - position2.x, 2) + math.pow(position1.y - position2.y, 2))


#############################################################
#                          CLASSES
#############################################################
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"


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
            phase = calculate_phase(txAnt.signal.frequency, txAnt.signal.phase, distance)
            self.signal = Signal(phase, rsl, txAnt.signal.frequency)
        else:
            print("reflected signal power = 0!")

class RxDipole(Dipole):
    def __init__(self, position, signal):
        super().__init__(position, signal)
        self.signal = signal
        self.reference_signal = Signal(0, 0, 0)

    def recieve_signal(self, txAnt, reference=False):
        if (txAnt.signal.power > 0):
            distance = calculate_distance(self.position, txAnt.position)
            current_fsl = calculate_fsl(distance, txAnt.signal.frequency)
            current_rsl = txAnt.signal.power - current_fsl

            if (reference):
                if (current_rsl > 0):
                    self.reference_signal.setPhase(calculate_phase(txAnt.signal.frequency, txAnt.signal.phase, distance))
                    self.reference_signal.power = current_rsl
                    self.reference_signal.frequency = txAnt.signal.frequency
                else:
                    print("reference signal RSL=0!")
            else:
                if (current_rsl > 0):
                    self.signal.setPhase(self.signal.phase + calculate_phase(txAnt.signal.frequency, txAnt.signal.phase, distance) * current_rsl / (current_rsl + self.signal.power))
                    self.signal.power += current_rsl
                else:
                    print("RSL=0")

    def get_normalized_signal(self):
        if self.reference_signal.power > 0 and self.signal.power != self.reference_signal.power:
            phase = (self.signal.phase * self.signal.power - self.reference_signal.phase * self.reference_signal.power) / (self.signal.power - self.reference_signal.power)
            power = self.signal.power - self.reference_signal.power
            return Signal(phase, power, self.signal.frequency)
        else:
            return self.signal

class RxAntennaArray:
    def __init__(self, dipoles):
        self.dipoles = dipoles


#############################################################
#                       INITIALIZATION
#############################################################
wavelength = 5
dipole_spread = 2
antenna_spread = 10

frequency = SPEED_OF_LIGHT/wavelength

# reciever antenna x,y center
dipoles1 = [
    RxDipole(Position((0              - antenna_spread) / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position((-dipole_spread - antenna_spread) / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position(( dipole_spread - antenna_spread) / 2, 0), Signal(0, 0, frequency))
]

dipoles2 = [
    RxDipole(Position((0              + antenna_spread) / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position((-dipole_spread + antenna_spread) / 2, 0), Signal(0, 0, frequency)),
    RxDipole(Position(( dipole_spread + antenna_spread) / 2, 0), Signal(0, 0, frequency))
]

antennas = [
    RxAntennaArray(dipoles1),
    RxAntennaArray(dipoles2)
]

# transmitter antenna x,y center
tx = TxDipole(Position(15, 20), Signal(phase=0, power=400, frequency=frequency))

# measured object x,y center
obj_position = Position(-10, 30)


#############################################################
#                        CALCULATION
#############################################################

reflect=True
if reflect:
    object = TxDipole(obj_position, is_reflector=True)
    object.reflect_signal(tx)
else:
    object = TxDipole(obj_position, Signal(phase=0, power=400, frequency=frequency))

#############################################################
#                         SIMULATION
#############################################################
for antenna in antennas:
    for dipole in antenna.dipoles:
        # dipole.recieve_signal(tx)
        # dipole.recieve_signal(tx, reference=True)

        dipole.recieve_signal(object)


#############################################################
#                           PLOTS
#############################################################
fig, ax = plt.subplots()
ax.set_aspect(1)

plot_line_between(ax, obj_position, tx.position, 'yellow')
ax.plot(obj_position.x, obj_position.y, color='black', marker='s')

for antenna in antennas:
    for dipole in antenna.dipoles:
        plot_antenna(ax, dipole, 'black')
        plot_line_between(ax, obj_position, dipole.position, 'yellow')

for i, antenna in enumerate(antennas):
    print(f"{i + 1}. antenna-to-object angle = {calculate_angle(antenna.dipoles[0].position, obj_position):.7f} deg.")

for i, antenna in enumerate(antennas):
    for j, dipole in enumerate(antenna.dipoles):
        signal = dipole.get_normalized_signal()
        print(f"{i + 1}. antenna, {j + 1}. dipole: phase={signal.phase:.7f} rsl={signal.power:.7f}")



angle = np.linspace(0, 2 * np.pi, 150)

how_many_circles = 7

regression_lines = []
for antenna in antennas:
    previous_variance = math.inf
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
                plot_point(ax, point)


        figure_center = calculate_figure_center(cross_points_of_circles)
        figure_centers.append(figure_center)

        # try to calculate position of object basing on changing variance
        current_variance = calculate_figure_center_variance(cross_points_of_circles)
        if current_variance > previous_variance:
            plot_point(ax, figure_center, 'cyan', '*')

            break
        else:
            previous_variance = current_variance

    slope, intercept = linear_regression(figure_centers)
    regression_lines.append([slope, intercept])
    plot_regression_line(ax, antenna.dipoles[0].position.x, slope, intercept, length=35)

# calculate position of object basing on linear regressions
line_parameters1, line_parameters2 = regression_lines
crossing_point = calculate_crossing_of_lines(line_parameters1, line_parameters2)
plot_point(ax, crossing_point, 'magenta', '*')

plot_antenna(ax, tx, 'green')



print("magenta asterisk - found by linear regression")
print("cyan asterisk    - found by changing variance of distances")

_ = ax.set_ylim(bottom=-1)
_ = ax.set_xlim(left=-20, right=20)
