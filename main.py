# %%
import matplotlib.pyplot as plt
import math
import numpy as np

# all lengths are in meters
# all time in seconds
# all angles in radians
# all powers in dB


SPEED_OF_LIGHT = 299792458


#############################################################
#                         FUNCTIONS
#############################################################
def get_intersections(circle0, circle1):
    x0, y0, r0 = circle0
    x1, y1, r1 = circle1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)

    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d
        y2=y0+a*(y1-y0)/d
        x3=x2+h*(y1-y0)/d
        y3=y2-h*(x1-x0)/d
        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        return x3, y3, x4, y4


def print_antenna(ax, antenna, color):
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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_distance(self, position):
        return math.sqrt(pow(self.x - position.x, 2) + pow(self.y - position.y, 2))


#############################################################
#                               CLASSES
#############################################################
class Signal():
    def __init__(self, phase, power, frequency):
        self.phase = wrap_phase(phase)
        self.power = power
        self.frequency = frequency

    def getWavelangth(self):
        return SPEED_OF_LIGHT/self.frequency

    def setPhase(self, phase):
        self.phase = wrap_phase(phase)



class Antenna:
    def __init__(self, position, signal):
        self.position = position
        self.signal = signal


class TxAnt(Antenna):
    def __init__(self, position, signal=Signal(0,0,0), is_reflector=False):
        super().__init__(position, signal)
        self.is_reflector = is_reflector

        if(is_reflector):
            self.signal = Signal(0, 0, 0)

    def reflect_signal(self, txAnt):
        distance = self.position.calculate_distance(txAnt.position)
        fsl = calculate_fsl(distance, txAnt.signal.frequency)
        rsl = txAnt.signal.power - fsl
        if (rsl > 0):
            phase = calculate_phase(txAnt.signal.frequency, txAnt.signal.phase, distance)
            self.signal = Signal(phase, rsl, txAnt.signal.frequency)
        else:
            print("reflected signal power = 0!")

class RxAnt(Antenna):
    def __init__(self, position, signal):
        super().__init__(position, signal)
        self.signal = signal
        self.reference_signal = Signal(0, 0, 0)

    def recieve_signal(self, txAnt, reference=False):
        if (txAnt.signal.power > 0):
            distance = self.position.calculate_distance(txAnt.position)
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


#############################################################
#                      INITIALIZATION
#############################################################
wavelength = 3.5
spread = 2

frequency = SPEED_OF_LIGHT/wavelength

# reciever antenna x,y center
dipoles = [
    RxAnt(Position(0, 0), Signal(0, 0, frequency)),
    RxAnt(Position(-spread, 0), Signal(0, 0, frequency)),
    RxAnt(Position( spread, 0), Signal(0, 0, frequency))
]

# transmitter antenna x,y center
tx = TxAnt(Position(15, -20), Signal(phase=0, power=400, frequency=frequency))

# measured object x,y center
# obj = [-4, -15]
obj_position = Position(-15, -30)


#############################################################
#                      CALCULATION
#############################################################

reflect=True
if reflect:
    object = TxAnt(obj_position, is_reflector=True)
    object.reflect_signal(tx)
else:
    object = TxAnt(obj_position, Signal(phase=0, power=400, frequency=frequency))

#############################################################
#                         SIMULATION
#############################################################

for dipole in dipoles:
    # dipole.recieve_signal(tx)
    # dipole.recieve_signal(tx, reference=True)

    dipole.recieve_signal(object)



#############################################################
#                           PLOTS
#############################################################
print(f"antenna coverage angle = {math.atan(wavelength/(2 * spread)) * 360 / (2 * math.pi):.7f}")
print(f"object angle = {math.atan(obj_position.x / obj_position.y) * 360 / (2 * math.pi):.7f}")

for i, dipole in enumerate(dipoles):
    signal = dipole.get_normalized_signal()
    print(f"{i} dipole: phase={signal.phase:.7f} rsl={signal.power:.7f}")

fig, ax = plt.subplots()
ax.set_aspect(1)

angle = np.linspace(0, 2 * np.pi, 150)

how_many_circles = 10

for i in range(how_many_circles):
    circles = []
    for dipole in dipoles:
        signal = dipole.get_normalized_signal()
        radius = (signal.phase / (2 * math.pi)) * signal.getWavelangth() + (i + 1)  * signal.getWavelangth()
        x =  radius * np.cos(angle) + dipole.position.x
        y =  radius * np.sin(angle) + dipole.position.y
        ax.plot(x, y, color='black')
        circles.append([dipole.position.x, dipole.position.y, radius])

    intersections = get_intersections(circles[0], circles[1])
    if intersections is not None:
        i_x0, i_y0, i_x1, i_y1 = intersections
        ax.plot(i_x0, i_y0, color='blue', marker='o')
        ax.plot(i_x1, i_y1, color='blue', marker='o')

    intersections = get_intersections(circles[1], circles[2])
    if intersections is not None:
        i_x0, i_y0, i_x1, i_y1 = intersections
        ax.plot(i_x0, i_y0, color='blue', marker='o')
        ax.plot(i_x1, i_y1, color='blue', marker='o')

    intersections = get_intersections(circles[0], circles[2])
    if intersections is not None:
        i_x0, i_y0, i_x1, i_y1 = intersections
        ax.plot(i_x0, i_y0, color='blue', marker='o')
        ax.plot(i_x1, i_y1, color='blue', marker='o')


plot_line_between(ax, obj_position, tx.position, 'yellow')

print_antenna(ax, tx, 'green')

ax.plot(obj_position.x, obj_position.y, color='red', marker='o')


for dipole in dipoles:
    print_antenna(ax, dipole, 'black')
    plot_line_between(ax, obj_position, dipole.position, 'yellow')


# %%
