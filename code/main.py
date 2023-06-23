import sys
import os
sys.path.append("algorithms")
sys.path.append("classes")
sys.path.append("visualisation")

from visualisation.visualiser import visualise
import algorithms.random_alg
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing as sa
from algorithms.astar import AstarAlg

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

    # Create output folder
    folder = f'../output/{output_filename}'

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        print("Please specify a unique output filename.")
        sys.exit(1)
    
    if (algorithm == "random"):
        # Run random algorithm
        print("Start Random")
        chip = random_alg.run_random(chip_number, netlist_number, output_filename)
        visualise(chip, algorithm, output_filename)
    elif (algorithm == "hillclimber"):
        # Run Hill Climber algorithm
        print("Start Hill Climber")
        hillclimber = HillClimber(chip_number, netlist_number, output_filename)
        chip = hillclimber.run()
        visualise(chip, algorithm, output_filename)
    elif (algorithm == "simulatedannealing"):
        # Run Simulated Annealing algorithm
        print("Start Simulated Annealing") 
        sim_annealing = sa(chip_number, netlist_number, output_filename, temp= 100000)
        sim_annealing.run_sim_annealing()
    elif (algorithm == "astar"):
        print("Start A*")
        astar = AstarAlg(chip_number, netlist_number, output_filename)
        chip = astar.chip
        visualise(chip, algorithm, output_filename)
    else:
        print("Invalid algorithm: Choose from random, hillclimber or astar")
        sys.exit(1)