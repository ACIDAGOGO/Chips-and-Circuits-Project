import sys
import csv
import matplotlib.pyplot as plt
import math
import statistics
import numpy as np

def calculate_optimal_bins(data):
    # Calculate the interquartile range (IQR)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    # Calculate the optimal bin width
    bin_width = 2 * iqr / math.pow(len(data), 1/3)

    # Round the bin width to the nearest integer
    bin_width = int(round(bin_width))

    # Calculate the number of bins
    data_range = max(data) - min(data)
    num_bins = int(data_range / bin_width)

    return bin_width, num_bins


if __name__ == "__main__":

     # Check if at least three command-line arguments are provided
    if len(sys.argv) >= 2:
        filename: str = sys.argv[1]
        path = f"../../output/{filename}"

    else:
        print("Insufficient command-line arguments. Please provide at least one argument: filename.")
        sys.exit(1)

    # Set up empty data containers
    iterations: list = []
    costs: list = []
    wirecounts: list = []
    intersectioncounts: list = []

    costcalculation: list = []

    with open(path) as file:
        reader = csv.reader(file)

        # Skip the first line
        next(reader)
        
        # Iterate over the csv file
        for row in reader:
            
            # Load data
            iterations.append(int(row[0]))
            costs.append(int(row[1]))
            wirecounts.append(int(row[2]))
            intersectioncounts.append(int(row[3]))
            costcalculation.append(int(row[2]) + 300 * int(row[3]))


    # Plotting histogram of total number of wire intersection
    bin_width, num_bins = calculate_optimal_bins(costs)

    # plt.hist(costs, bins=range(0, bin_width * num_bins, bin_width))
    plt.hist(costs, bins=range(min(costs), max(costs) + bin_width, bin_width), linewidth = 1.2, edgecolor = 'black')
    plt.suptitle(f"Frequency of total chip costs over {len(iterations)} iterations", fontsize = 12)
    plt.title(f"Mean = {round(statistics.mean(costs))}, Min = {min(costs)}, Max = {max(costs)}", fontsize = 10)
    plt.xlabel("Total cost of chip configuration")
    plt.ylabel("Frequency")
    plt.show()


    # Plotting histogram of total number of wire intersection
    bin_width, num_bins = calculate_optimal_bins(intersectioncounts)

    plt.hist(intersectioncounts, bins=range(min(intersectioncounts), max(intersectioncounts) + bin_width, bin_width), linewidth = 1.2, edgecolor = 'black')
    plt.suptitle(f"Frequency of total amount of wire intersections over {len(iterations)} iterations", fontsize = 12)
    plt.title(f"Mean = {round(statistics.mean(intersectioncounts))}, Min = {min(intersectioncounts)}, Max = {max(intersectioncounts)}", fontsize = 10)
    plt.xlabel("Total number of wire intersections on chip")
    plt.ylabel("Frequency")
    plt.show()


    # Plotting histogram of total number of wires
    bin_width, num_bins = calculate_optimal_bins(wirecounts)

    plt.hist(wirecounts, bins=range(min(wirecounts), max(wirecounts) + bin_width, bin_width), linewidth = 1.2, edgecolor = 'black')
    plt.suptitle(f"Frequency of total wire units over {len(iterations)} iterations", fontsize = 12)
    plt.title(f"Mean = {round(statistics.mean(wirecounts))}, Min = {min(wirecounts)}, Max = {max(wirecounts)}", fontsize = 10)
    plt.xlabel("Total number of wire units on chip")
    plt.ylabel("Frequency")
    plt.show()