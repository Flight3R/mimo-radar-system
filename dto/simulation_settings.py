class SimulationSettings:
    def __init__(self, detection_method, phase_increment, wavelength, phase_error_coefficient):
        self.detection_method = detection_method
        self.phase_increment = phase_increment
        self.wavelength = wavelength
        self.phase_error_coefficient = phase_error_coefficient

    def __str__(self):
        return f"Detection method: {self.detection_method}, Phase increment: {self.phase_increment}, Wavelength: {self.wavelength}, Phase error coefficient: {self.phase_error_coefficient}"
