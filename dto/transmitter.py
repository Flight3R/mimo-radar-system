class Transmitter:
    def __init__(self, index, name, position, phase, power):
        self.index = index
        self.name = name
        self.position = position
        self.phase = phase
        self.power = power

    def __str__(self):
        return f"Transmitter(name={self.name}, position={self.position}, power={self.power})"