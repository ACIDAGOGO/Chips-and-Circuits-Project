import json
import sys
sys.path.append("classes")

from chip import Chip

def save_to_file(chip: 'Chip', output_filename: str):
    # to_json(chip.grid)
    json_data = json.dumps(chip.__dict__, skipkeys=True)

    with open(f'../output/{output_filename}.json', "a") as file:
        file.write(json_data + "\n")
