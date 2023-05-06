class Antenna:
    def __init__(self, index, name, position, dipole_number, dipole_spread):
        self.index = index
        self.name = name
        self.position = position
        self.dipole_number = dipole_number
        self.dipole_spread = dipole_spread

    def __str__(self):
        return f"Antenna(name={self.name}, position={self.position}, dipole_number={self.dipole_number}, dipole_spread={self.dipole_spread})"