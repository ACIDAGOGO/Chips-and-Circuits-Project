import sys
import csv
import matplotlib.pyplot as plt
import math


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

    amount_of_bins = int(math.sqrt(len(iterations)))
    # bins_count = list(range(min(costs), max(costs) + 1000, 1000))
    plt.hist(intersectioncounts, bins=amount_of_bins)
    plt.show()
    print(amount_of_bins)
    print(max(costs))