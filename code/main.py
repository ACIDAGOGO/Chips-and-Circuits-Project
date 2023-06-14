import sys
sys.path.append("algorithms")
sys.path.append("classes")
sys.path.append("visualisation")

from visualiser import visualise
import random_alg

if __name__ == "__main__":
    
    # Run random algorithm
    chip = random_alg.run_random()
    visualise(chip)