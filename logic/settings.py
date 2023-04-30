class Settings:
    def __init__(self, show_names, show_circles, show_lines, show_real_object, show_detected_object):
        self.show_names = show_names
        self.show_circles = show_circles
        self.show_lines = show_lines
        self.show_real_object = show_real_object
        self.show_detected_object = show_detected_object

    def __str__(self):
        return f"show_names={self.show_names}, show_circles={self.show_circles}, show_lines={self.show_lines}, show_real_object={self.show_real_object}, show_detected_object={self.show_detected_object}"
