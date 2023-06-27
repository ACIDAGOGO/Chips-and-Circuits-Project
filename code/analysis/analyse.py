import sys
import os
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


# if __name__ == "__main__":

#     # Check if at least three command-line arguments are provided
#     if len(sys.argv) >= 2:
#         filename: str = sys.argv[1]
#         filepath: str = f"../../output/{os.path.splitext(filename)}/{filename}"

#     else:
#         print("Insufficient command-line arguments. Please provide at least one argument: filename.")
#         sys.exit(1)

#     # Set up empty data containers
#     iterations: list[int] = []
#     costs: list[int] = []
#     wirecounts: list[int] = []
#     intersectioncounts: list[int] = []

#     with open(filepath) as file:
#         reader = csv.reader(file)

#         # Skip the first line
#         next(reader)

#         # Iterate over the csv file
#         for row in reader:

#             # Load data
#             iterations.append(int(row[0]))
#             costs.append(int(row[1]))
#             wirecounts.append(int(row[2]))
#             intersectioncounts.append(int(row[3]))

#     # Get optimal bin width
#     bin_width = calculate_optimal_bin_width(costs)

#     # Plot histogram of total costs over all iterations (suitable for random algorithm data)
#     plt.hist(costs, bins=range(min(costs), max(costs) + bin_width, bin_width), linewidth=1.2, edgecolor='black')
#     plt.suptitle(f"Frequency of total chip costs over {len(iterations)} iterations", fontsize=12)
#     plt.title(f"Mean = {round(statistics.mean(costs))}, Min = {min(costs)}, Max = {max(costs)}", fontsize=10)
#     plt.xlabel("Total cost of chip configuration")
#     plt.ylabel("Frequency")
#     plt.show()

    # # Plot histogram of total number of wire intersection
    # bin_width, num_bins = calculate_optimal_bins(intersectioncounts)

    # plt.hist(intersectioncounts, bins=range(min(intersectioncounts), max(intersectioncounts) + bin_width, bin_width), linewidth=1.2, edgecolor='black')
    # plt.suptitle(f"Frequency of total amount of wire intersections over {len(iterations)} iterations", fontsize=12)
    # plt.title(f"Mean = {round(statistics.mean(intersectioncounts))}, Min = {min(intersectioncounts)}, Max = {max(intersectioncounts)}", fontsize=10)
    # plt.xlabel("Total number of wire intersections on chip")
    # plt.ylabel("Frequency")
    # plt.show()

    # # Plot histogram of total number of wires
    # bin_width, num_bins = calculate_optimal_bins(wirecounts)

    # plt.hist(wirecounts, bins=range(min(wirecounts), max(wirecounts) + bin_width, bin_width), linewidth=1.2, edgecolor='black')
    # plt.suptitle(f"Frequency of total wire units over {len(iterations)} iterations", fontsize=12)
    # plt.title(f"Mean = {round(statistics.mean(wirecounts))}, Min = {min(wirecounts)}, Max = {max(wirecounts)}", fontsize=10)
    # plt.xlabel("Total number of wire units on chip")
    # plt.ylabel("Frequency")
    # plt.show()

    # Scatter plot to show how costs decline after a certain amount of iterations
    # plt.scatter(iterations, costs)
    # plt.show()

def load_data(output_filename: str) -> tuple[list[int], list[int], list[int], list[int], list[float], list[float]]:
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

    return iterations, costs, wirecounts, intersectioncounts, time_per_iteration, cumulative_time

# Only suitable for random algorithm data
def create_histogram(output_filename: str) -> None:
    # Get data
    data = load_data(output_filename)
    iterations = data[0]
    costs = data[1]

    # Get optimal bin width
    bin_width = calculate_optimal_bin_width(costs)

    # Plot histogram of total costs over all iterations (suitable for random algorithm data)
    plt.figure(figsize=(8,8))
    plt.hist(costs, bins=range(min(costs), max(costs) + bin_width, bin_width), linewidth=1.2, edgecolor='black')
    plt.title(f"Frequency of total chip costs over {len(iterations)} iterations (Random Algorithm)\nMean = {round(statistics.mean(costs))}, Min = {min(costs)}, Max = {max(costs)}", fontsize=15)
    plt.xlabel("Total cost of chip configuration", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.savefig(f'./../output/{output_filename}/{output_filename}_histogram.png', bbox_inches='tight', pad_inches=1, dpi=300)

def create_lineplot(output_filename: str, alg_name: str) -> None:
    # Get data
    data = load_data(output_filename)
    iterations = data[0]
    costs = data[1]
    wirecounts = data[2]
    intersectioncounts = data[3]

    # plot lineplot of total costs over iterations (suitable for comparing hillclimbing to simulated annealing
    plt.figure(figsize=(8,8))
    plt.plot(iterations, costs)
    plt.title(f"Total chip costs over {len(iterations)} iterations ({alg_name} Algorithm)", fontsize=15)
    plt.xlabel("Total cost of chip configuration", fontsize=12)
    plt.ylabel("Iterations", fontsize=12)
    plt.savefig(f'./../output/{output_filename}/{output_filename}_lineplot.png', bbox_inches='tight', pad_inches=1, dpi=300)
    
