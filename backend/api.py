from backend.definitions import *
from dto.antenna import Antenna
from dto.object import Object
from dto.position import PositionDto
from dto.simulation_settings import SimulationSettings
from dto.transmitter import Transmitter


class PositionIsNoneError(Exception):
    pass


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
        raise PositionIsNoneError

    return PositionDto(detected_position.x, detected_position.y)


def create_heatmap(antennas_dto: list[Antenna], transmitters_dto: list[Transmitter], settings: SimulationSettings,
                   edge_length, resolution, step_function, end_function):
    antennas: list[RxAntennaArray] = []
    for antenna_dto in antennas_dto:
        antennas.append(create_antenna(antenna_dto.dipole_number, antenna_dto.dipole_spread,
                                       settings.wavelength, map_position(antenna_dto.position)))

    transmitters: list[TxDipole] = []
    for transmitter_dto in transmitters_dto:
        transmitters.append(
            create_transmitter(transmitter_dto.phase, settings.wavelength, map_position(transmitter_dto.position)))

    method = select_detection_method(settings.detection_method)
    method_name = settings.detection_method
    phase_error_coef = settings.phase_error_coefficient

    return create_heat_map(edge_length, resolution, method, method_name, antennas, transmitters[0], phase_error_coef,
                           step_function, end_function)


def create_heat_map(edge_length: float, resolution: float, method, method_name: str, antennas: list, tx: TxDipole,
                    phase_error_coef, step_function, end_function):
    antennas_center = calculate_figure_center([ant.antenna_center for ant in antennas])
    x_min = antennas_center.x - edge_length / 2
    x_max = antennas_center.x + edge_length / 2
    y_min = antennas_center.y - edge_length / 2
    y_max = antennas_center.y + edge_length / 2
    x_space = np.arange(x_min, x_max, resolution)
    y_space = np.arange(y_min, y_max, resolution)
    heat_map = np.zeros((len(x_space), len(y_space)))

    complexity = (len(x_space) * len(y_space))
    iterator = 0
    print(f"heatmap_complexity={complexity}")

    for xi, x in enumerate(x_space):
        for yi, y in enumerate(y_space):
            obj_position = Position(x, y)
            object = TxDipole(obj_position, is_reflector=True)
            simulate(antennas, tx, object, phase_error_coef)
            target_position = detect_object_phase_increment(method, antennas, tx, object, phase_error_coef)
            pos_err = calculate_distance(target_position, obj_position)
            result = pos_err if pos_err is not None else np.inf
            heat_map[xi, yi] = result

            iterator += 1
            step_function(complexity, iterator)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    mesh = ax.pcolormesh(x_space, y_space, np.transpose(heat_map), cmap='jet')
    ax.set_title(f"Heatmap of {method_name} method\n{edge_length=}m, {resolution=}m")
    cbar = fig.colorbar(mesh, ax=ax)
    cbar.set_label("Position error [m]")

    filename = 'heatmap.png'
    fig.savefig(filename)
    end_function(filename)
