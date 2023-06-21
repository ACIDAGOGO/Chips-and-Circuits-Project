import sys
import matplotlib.pyplot as plt  # type: ignore
from matplotlib.pyplot import cm  # type: ignore
from chip import Chip  # type: ignore
import numpy as np
sys.path.append("./classes")


def get_gates(chip: 'Chip') -> tuple[list[int], list[int], list[int]]:
    """
    Return gate coordinates of a given chip.
    """
    coords_list: list = []

    for gate in chip.gates.values():
        coords_list.append(gate.get_coords())

    return extract_xyz(coords_list)


def get_wires(chip: 'Chip') -> list[list[tuple[int, int, int]]]:
    """
    Return paths of all wires of a given chip.
    """
    paths: list[list[tuple[int, int, int]]] = []

    for wire in chip.wires:
        path = wire.get_path()
        paths.append(path)

    return paths


def extract_xyz(coords: list[tuple[int, int, int]]) -> tuple[list[int], list[int], list[int]]:
    """
    Break up list of tuples into three seperate lists.
    """
    x: list = []
    y: list = []
    z: list = []

    for xyz in coords:
        x.append(xyz[0])
        y.append(xyz[1])
        z.append(xyz[2])

    return x, y, z


def visualise(chip: 'Chip', algorithm: str) -> None:
    """
    Plot given chip configuration in a 3D coloured scatterplot.
    """
    plt.style.use('_mpl-gallery')

    gates = get_gates(chip)

    # Plot gates
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.scatter(gates[0], gates[1], gates[2], color='black')

    # Plot gate numbers next to gates on grid
    for i in range(len(gates[0])):
        ax.text(gates[0][i], gates[1][i], gates[2][i], ' ' + str(i + 1))

    # Set title
    plt.title(f"Chip {chip.chip_no} - {chip.netlist_name} - Algorithm: {algorithm} - Cost: {chip.calculate_costs()}")

    # Get wire paths
    paths = get_wires(chip)

    # Create color for each wire
    colors = iter(cm.rainbow(np.linspace(0, 1, len(paths))))
    for path in paths:
        x, y, z = extract_xyz(path)
        c = next(colors)

        # Plot wires
        ax.plot(x, y, z, color=c)

    # Set adaptive plot size
    x, y, z = chip.grid.get_grid_size()
    ax.set_xlim(0, x)
    ax.set_ylim(0, y)
    ax.set_zlim(0, z)
    ax.set_xticks(range(0, x + 1))
    ax.set_yticks(range(0, y + 1))
    ax.set_zticks(range(0, z + 1))

    plt.show()
