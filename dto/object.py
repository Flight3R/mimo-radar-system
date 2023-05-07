class Object:
    def __init__(self, index, name, position):
        self.index = index
        self.name = name
        self.position = position

    def __str__(self):
        return f"Object(name={self.name}, position={self.position})"