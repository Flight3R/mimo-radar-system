class Transmitter:
    def __init__(self, index, name, position, phase):
        self.index = index
        self.name = name
        self.position = position
        self.phase = phase

    def __str__(self):
        return f"Transmitter(name={self.name}, position={self.position}, phase={self.phase})"