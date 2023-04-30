class Object:
    def __init__(self, name, coordinates, reflection):
        self.name = name
        self.coordinates = coordinates
        self.reflection = reflection

    def __str__(self):
        return f"Object(name={self.name}, coordinates={self.coordinates}, reflection={self.reflection})"