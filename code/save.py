import csv
import sys
sys.path.append("classes")

from chip import Chip

def extract_data(chip: 'Chip') -> list[int]:
    data: list = []

    # Adds iteration, cost, wirecount, intersectioncount to data list
    data.append(chip.iteration)
    data.append(chip.cost)
    data.append(chip.wirecount)
    data.append(chip.intersectioncount)

    return data


def save_to_file(chip: 'Chip', output_filename: str):
    data = extract_data(chip)

    # Opens output file and appends latest chip iteration data
    with open(f'../output/{output_filename}.csv', "a", newline = "") as file:
        writer = csv.writer(file)
        if data[0] == 0:
            writer.writerow(["iteration","cost","wirecount","intersectioncount"])

        writer.writerow(data)
