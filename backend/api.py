from backend.definitions import *
from dto.antenna import Antenna
from dto.object import Object
from dto.position import PositionDto
from dto.simulation_settings import SimulationSettings
from dto.transmitter import Transmitter


def map_position(position: PositionDto) -> Position:
    return Position(position.x, position.y)


def create_antenna(dipole_number: int, dipole_spread: int, wavelength: float,
                   center_position: Position) -> RxAntennaArray:
    dipoles = []
    frequency = SPEED_OF_LIGHT / wavelength
    center_x, center_y = center_position.x, center_position.y
    min_x = center_x - ((dipole_number - 1) * dipole_spread) / 2
    max_x = center_x + ((dipole_number - 1) * dipole_spread) / 2
    for x in np.linspace(min_x, max_x, dipole_number):
        dipoles.append(RxDipole(Position(x, center_y), Signal(0, 0, frequency)))
    return RxAntennaArray(dipoles)


def create_transmitter(phase_offset: float, wavelength: float, position: Position) -> TxDipole:
    frequency = SPEED_OF_LIGHT / wavelength
    return TxDipole(position, Signal(phase=phase_offset, power=1, frequency=frequency))


def create_object(position: Position) -> TxDipole:
    return TxDipole(Position(position.x, position.y), is_reflector=True)


def detect_by_method(method, phase_increment: bool, antennas: list, tx: TxDipole, object: TxDipole,
                     phase_error_coef=0.0) -> Position:
    if phase_increment:
        return detect_object_phase_increment(method, antennas, tx, object, phase_error_coef)
    else:
        simulate(antennas, tx, object, phase_error_coef)
        return method(antennas, tx, object.position)


def detect(object_dto: Object, antennas_dto: list[Antenna], transmitters_dto: list[Transmitter],
           settings: SimulationSettings):
    object = create_object(map_position(object_dto.position))

    antennas: list[RxAntennaArray] = []
    for antenna_dto in antennas_dto:
        antennas.append(create_antenna(antenna_dto.dipole_number, antenna_dto.dipole_spread,
                                       settings.wavelength, map_position(antenna_dto.position)))

    transmitters: list[TxDipole] = []
    for transmitter_dto in transmitters_dto:
        transmitters.append(
            create_transmitter(transmitter_dto.phase, settings.wavelength, map_position(transmitter_dto.position)))

    method = select_detection_method(settings.detection_method)
    phase_increment: bool = settings.phase_increment == "yes"
    phase_error_coef = settings.phase_error_coefficient

    detected_position = detect_by_method(method, phase_increment, antennas, transmitters[0], object, phase_error_coef)

    if detected_position is None:
        print("Position is none")
    return PositionDto(detected_position.x, detected_position.y)
