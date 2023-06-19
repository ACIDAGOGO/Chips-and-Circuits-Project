import json
import sys
sys.path.append("classes")

from chip import Chip
from grid import Grid

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is of a non-serializable type
        if isinstance(obj, Grid):
            # Provide custom serialization logic for NonSerializableClass
            return obj.to_json()

        # For other types, use the default serialization behavior
        return super().default(obj)


def save_to_file(chip: 'Chip', output_filename: str):
    json_data = json.dumps(chip, default=MyEncoder)

    with open(f'../output/{output_filename}.json', "a") as file:
        file.write(json_data + "\n")
