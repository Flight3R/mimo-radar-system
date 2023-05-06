class Object:
    def __init__(self, index, name, position, reflection):
        self.index = index
        self.name = name
        self.position = position
        self.reflection = reflection

    def __str__(self):
        return f"Object(name={self.name}, position={self.position}, reflection={self.reflection})"