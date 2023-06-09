import csv
import matplotlib.pyplot as plt  # type: ignore
import math
import statistics
import numpy as np


def calculate_optimal_bin_width(data: list[int]) -> int:
    """
    Calculate the optimal bin width given the data characteristics.
    """

    # Calculate the interquartile range (IQR)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    # Calculate the optimal bin width
    bin_width: int = round(2 * iqr / math.pow(len(data), 1/3))

    return bin_width


def load_data(output_filename: str) ->\
              tuple[list[int], list[int], list[int], list[int],
                    list[float], list[float]]:
    """
    Loads data from csv-file and stores it in lists.
    """

    filename: str = output_filename
    filepath: str = f"./../output/{filename}/{filename}.csv"

    # Set up empty data containers
    iterations: list[int] = []
    costs: list[int] = []
    wirecounts: list[int] = []
    intersectioncounts: list[int] = []
    time_per_iteration: list[float] = []
    cumulative_time: list[float] = []

    with open(filepath) as file:
        reader = csv.reader(file)

        # Skip the first line
        next(reader)

        # Iterate over the csv file
        for row in reader:

            # Load data into lists
            iterations.append(int(row[0]))
            costs.append(int(row[1]))
            wirecounts.append(int(row[2]))
            intersectioncounts.append(int(row[3]))
            time_per_iteration.append(float(row[4]))
            cumulative_time.append(float(row[5]))

    return iterations, costs, wirecounts, intersectioncounts,\
        time_per_iteration, cumulative_time


def create_histogram(output_filename: str) -> None:
    """
    Creates a histrogram from csv-file.
    (only suitable for random algorithm data)
    """

    # Get data
    data = load_data(output_filename)
    iterations = data[0]
    costs = data[1]

    # Get optimal bin width
    bin_width = calculate_optimal_bin_width(costs)

    # Plot histogram of total costs over all iterations
    # (suitable for random algorithm data)
    plt.figure(figsize=(8, 8))
    plt.hist(costs, bins=range(min(costs), max(costs) + bin_width, bin_width),
             linewidth=1.2, edgecolor='black')
    plt.title(f"Frequency of total chip costs over {len(iterations)}"\
              f" iterations (Random Algorithm)\n"\
              f" Mean = {round(statistics.mean(costs))},"\
              f" Min = {min(costs)}, Max = {max(costs)}", fontsize=15)
    plt.xlabel("Total cost of chip configuration", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.savefig(f"./../output/{output_filename}/"\
                f"{output_filename}_histogram.png",
                bbox_inches='tight', pad_inches=1, dpi=300)


def create_lineplot(output_filename: str, alg_name: str) -> None:
    """
    Creates a lineplot from csv-file.
    (suitable for comparing hillclimbing to simulated annealing)
    """

    # Get data
    data = load_data(output_filename)
    iterations = data[0]
    costs = data[1]

    maximum = max(iterations)

    # Determine last iteration and cost
    for index, value in enumerate(iterations):
        if value == maximum:
            cost = costs[index]
            iteration = iterations[index]

    # Plot lineplot of total costs over iterations
    plt.figure(figsize=(8, 8))
    plt.plot(iterations, costs)
    plt.title(f"Total chip costs over {iteration}"
               f" iterations ({alg_name} Algorithm)", fontsize=15)
    plt.xlabel("Iterations", fontsize=12)
    plt.ylabel("Total cost of chip configuration", fontsize=12)
    plt.text(maximum, cost, str(cost))
    plt.savefig(f"./../output/{output_filename}/{output_filename}_lineplot.png",
                bbox_inches='tight', pad_inches=1, dpi=300)
