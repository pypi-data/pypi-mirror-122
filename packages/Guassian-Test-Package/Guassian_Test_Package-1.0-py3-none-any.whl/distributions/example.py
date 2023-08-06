import pathlib
from pathlib import Path

from distributions.gaussian import Gaussian

parent_path = pathlib.Path().resolve()
numbers_file_path = Path(str(parent_path) + "/numbers.txt")

"""Examples"""

mu = 5
std = 2

# Get first distribution
g1 = Gaussian(mu=mu,
              sigma=std)

# Get second distribution by passing list of numbers
g2 = Gaussian(numbers=[3, 9, 10])

# Get third distribtion from reading from the file
g3 = Gaussian(from_file=True)

g3.read_data_file(file_name=numbers_file_path)

# Printing the means from three distribution
print(g1.mu)
print(g2.mu)
print(g3.mu)
