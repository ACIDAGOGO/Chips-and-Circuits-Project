import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import cm
sys.path.append("./classes")
from chip import Chip

def get_gates(chip: 'Chip') -> tuple[list[int], list[int], list[int]]:
    gate_coords: list[tuple[int, int, int]] = []
    coords_list: list = []

    for gate in chip.gates.values():
        coords_list.append(gate.get_coords())
        
    return extract_xyz(coords_list)


def get_wires(chip: 'Chip') -> list[list[tuple[int, int, int]]]:
    paths: list[list[tuple[int, int, int]]] = []

    for wire in chip.wires:
        path = wire.get_path()
        paths.append(path)

    return paths


def extract_xyz(coords: list[tuple[int, int, int]]) -> tuple[list[int], list[int], list[int]]:
    x: list = []
    y: list = []
    z: list = []

    for xyz in coords:
        x.append(xyz[0])
        y.append(xyz[1])
        z.append(xyz[2])

    return x, y, z


def visualise(chip: 'Chip') -> None:
    plt.style.use('_mpl-gallery')

    gates = get_gates(chip)

    # Plot gates
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax.scatter(gates[0], gates[1], gates[2], color='red')

    # Plot wires
    # Get paths
    paths = get_wires(chip)

    # Create color for each wire
    colors = iter(cm.rainbow(np.linspace(0, 1, len(paths))))
    for path in paths:
        x, y, z = extract_xyz(path)
        c = next(colors)
        ax.plot(x, y, z, color=c)


    ax.set(xticklabels=[],
        yticklabels=[],
        zticklabels=[])

    plt.show()
