import sys
sys.path.append("algorithms")
sys.path.append("classes")
sys.path.append("visualisation")

from visualiser import visualise
import random_alg
from hill_climber import HillClimber

if __name__ == "__main__":
    
    # Check if at least three command-line arguments are provided
    if len(sys.argv) >= 5:
        chip_number: int = int(sys.argv[1])
        netlist_number: int = int(sys.argv[2])
        algorithm: str = sys.argv[3]
        output_filename: str = sys.argv[4]
    else:
        print("Insufficient command-line arguments. Please provide at least four arguments: chip number, netlist number, algorithm, output filename.")
        sys.exit(1)

    if chip_number not in [0, 1, 2]:
        print("Chip number not valid.")
        sys.exit(1)

    # Create list for allowed netlists
    allowed_netlist_numbers = range(chip_number * 3 + 1, chip_number * 3 + 4)

    # Check if specified netlist falls within list
    if netlist_number not in allowed_netlist_numbers:
        print("Netlist number not valid.")
        sys.exit(1)
    
    # Run random algorithm
    # print("start run")
    # chip = random_alg.run_random(chip_number, netlist_number, output_filename)
    # visualise(chip, algorithm)

    # Run Hill Climber algorithm
    hillclimber = HillClimber(chip_number, netlist_number, output_filename)
    hillclimber.run()