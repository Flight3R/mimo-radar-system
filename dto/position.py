class PositionDto:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"Position(x={self.x}, y={self.y})"
