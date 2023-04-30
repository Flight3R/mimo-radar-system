class Transmitter:
    def __init__(self, name, coordinates, power):
        self.name = name
        self.coordinates = coordinates
        self.power = power

    def __str__(self):
        return f"Transmitter(name={self.name}, coordinates={self.coordinates}, power={self.power})"