class Antenna:
    def __init__(self, index, name, coordinates, dipole_number, dipole_spread):
        self.index = index
        self.name = name
        self.coordinates = coordinates
        self.dipole_number = dipole_number
        self.dipole_spread = dipole_spread

    def __str__(self):
        return f"Antenna(name={self.name}, coordinates={self.coordinates}, dipole_number={self.dipole_number}, dipole_spread={self.dipole_spread})"