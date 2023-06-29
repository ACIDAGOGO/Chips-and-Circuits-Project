from visualisation.visualiser import visualise
from algorithms.random_alg import run_random
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing as sa
from algorithms.astar import AstarAlg
from analysis.analyse import create_histogram, create_lineplot
import sys
import os
sys.path.append("algorithms")
sys.path.append("classes")
sys.path.append("visualisation")
sys.path.append("analysis")


if __name__ == "__main__":
    # Check if at least three command-line arguments are provided
    if len(sys.argv) >= 5:
        chip_number: int = int(sys.argv[1])
        netlist_number: int = int(sys.argv[2])
        algorithm: str = sys.argv[3]
        output_filename: str = sys.argv[4]
        if len(sys.argv) >= 6:
            sorting_mode: str = sys.argv[5]
            if len(sys.argv) >= 7:
                heuristic: str = sys.argv[6]
            else:
                heuristic = None
        else:
            sorting_mode = None
            heuristic = None

        endmessage = f"Run completed. Output can be found in:"\
                      f" Chips-and-Circuits-Project/output/{output_filename}/"
    else:
        print("Insufficient command-line arguments."\
               " Please provide at least four arguments:"\
               " chip number, netlist number, algorithm, output filename.")
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
    folder = f"../output/{output_filename}"

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        print("Please specify a unique output filename.")
        sys.exit(1)

    # Check if valid sorting mode is given
    if (sorting_mode not in [None, "ascending", "descending"]):
        print("Invalid heuristic. Choose from: ascending, descending")
        sys.exit(1)

    # Check if valid heuristic is given
    if (heuristic not in [None, "avoid_gates", "avoid_low", "all"]):
        print("Invalid heuristic. Choose from: avoid_gates, avoid_low, all")
        sys.exit(1)

    if (algorithm == "random"):
        print("Started Random\nPress 'ctrl+C' to end run")

        # Run random algorithm
        chip = run_random(chip_number, netlist_number, output_filename)
        visualise(chip, algorithm, output_filename)
        create_histogram(output_filename)

        print(endmessage)
    elif (algorithm == "hillclimber"):
        print("Started Hill Climber\nPress 'ctrl+C' to end run")

        # Run Hill Climber algorithm
        hillclimber = HillClimber(chip_number, netlist_number, output_filename)
        chip = hillclimber.run()
        visualise(chip, algorithm, output_filename)
        create_lineplot(output_filename, "Hillclimber")

        print(endmessage)
    elif (algorithm == "simulatedannealing"):
        print("Started Simulated Annealing\nPress 'ctrl+C' to end run")

        # Run Simulated Annealing algorithm
        sim_annealing = sa(chip_number, netlist_number, output_filename,
                           temp=100000)
        chip = sim_annealing.run_sim_annealing()
        visualise(chip, algorithm, output_filename)
        create_lineplot(output_filename, "Simulated Annealing")

        print(endmessage)
    elif (algorithm == "astar"):
        print("Started A*")

        # Run A* algorithm
        astar = AstarAlg(chip_number, netlist_number, output_filename,
                         sorting_mode, heuristic)
        chip = astar.chip
        algorithm_name = f"{algorithm} - Sort: {sorting_mode}"\
                          f" - Heuristic: {heuristic}"
        visualise(chip, algorithm_name, output_filename)

        print(endmessage)
    else:
        print("Invalid algorithm:"\
               " Choose from random, hillclimber, simulatedannealing or astar.")
        sys.exit(1)
