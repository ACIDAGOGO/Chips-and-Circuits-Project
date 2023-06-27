import csv
import sys

from typing import Union
from classes.chip import Chip  # type: ignore
sys.path.append("../classes")


def extract_data(chip: 'Chip') -> list[Union[int, float]]:
    """
    Grab iteration number, total cost, total wirecount
    and intersectioncount from chip. Return it as list.
    """
    data: list[Union[int, float]] = []

    data.append(int(chip.iteration))
    data.append(int(chip.cost))
    data.append(int(chip.wirecount))
    data.append(int(chip.intersectioncount))
    data.append(float(chip.iteration_duration))
    data.append(float(chip.cumulative_duration))

    return data


def save_to_file(chip: 'Chip', output_filename: str) -> None:
    """
    Write data from list to csv file.
    """
    data = extract_data(chip)

    # Open output file and append latest chip iteration data
    with open(f'../output/{output_filename}/{output_filename}.csv', "a", newline="") as file:
        writer = csv.writer(file)
        if data[0] == 0:
            writer.writerow(["iteration", "cost", "wirecount", "intersectioncount", "time_per_iteration", "cumulative_time"])

        writer.writerow(data)
