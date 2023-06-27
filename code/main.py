import sys
import os
sys.path.append("algorithms")
sys.path.append("classes")
sys.path.append("visualisation")
sys.path.append("analysis")

from visualisation.visualiser import visualise
from algorithms.random_alg import *
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing as sa
from algorithms.astar import AstarAlg
from analysis.analyse import *

if __name__ == "__main__":
    
    # Check if at least three command-line arguments are provided
    if len(sys.argv) >= 5:
        chip_number: int = int(sys.argv[1])
        netlist_number: int = int(sys.argv[2])
        algorithm: str = sys.argv[3]
        output_filename: str = sys.argv[4]
        endmessage = f"Run completed. Output can be found in Chips-and-Circuits-Project/output/{output_filename}/"
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
        print("Started Random\nPress 'ctrl+C' to end run")
        chip = run_random(chip_number, netlist_number, output_filename)
        visualise(chip, algorithm, output_filename)
        create_histogram(output_filename)
        print(endmessage)

    elif (algorithm == "hillclimber"):
        # Run Hill Climber algorithm
        print("Started Hill Climber\nPress 'ctrl+C' to end run")
        hillclimber = HillClimber(chip_number, netlist_number, output_filename)
        chip = hillclimber.run()
        visualise(chip, algorithm, output_filename)
        create_lineplot(output_filename, "Hillclimber")
        print(endmessage)
        
    elif (algorithm == "simulatedannealing"):
        # Run Simulated Annealing algorithm
        print("Started Simulated Annealing\nPress 'ctrl+C' to end run") 
        sim_annealing = sa(chip_number, netlist_number, output_filename, temp= 100000)
        sim_annealing.run_sim_annealing()
        create_lineplot(output_filename, "Simulated Annealing")
        print(endmessage)

    elif (algorithm == "astar"):
        print("Started A*")
        astar = AstarAlg(chip_number, netlist_number, output_filename, None)
        chip = astar.chip
        #visualise(chip, algorithm, output_filename)
        print(endmessage)

        astar = AstarAlg(chip_number, netlist_number, output_filename, "avoid_gates")
        chip = astar.chip
        #visualise(chip, "avoid gates", output_filename)
        print(endmessage)

        astar = AstarAlg(chip_number, netlist_number, output_filename, "avoid_low")
        chip = astar.chip
        #visualise(chip, "avoid low", output_filename)
        print(endmessage)

        astar = AstarAlg(chip_number, netlist_number, output_filename, "all")
        chip = astar.chip
        #visualise(chip, "avoid all", output_filename)
        print(endmessage)

    else:
        print("Invalid algorithm: Choose from random, hillclimber, simulatedannealing or astar.")
        sys.exit(1)