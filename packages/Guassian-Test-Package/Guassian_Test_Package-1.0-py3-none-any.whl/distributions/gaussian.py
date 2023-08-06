import math
from pathlib import Path
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np

from distributions.distribution import Distribution


class Gaussian(Distribution):
    """A package to calculate gaussian distribution and probabilities"""

    def __init__(self, numbers: Optional[List[float]] = None, mu: float = None,
                 sigma: float = None, from_file: bool = False) -> None:
        super().__init__(mu=mu, sigma=sigma)

        if mu is not None and sigma is not None and numbers is None:
            self.mu = mu
            self.sigma = sigma

        elif (mu is None and sigma is None) and numbers is not None:
            self.numbers = numbers
            self.mu = np.mean(self.numbers)
            self.sigma = np.std(self.numbers)

        elif from_file:
            self.data = []

        else:
            raise ValueError("""Cannot compute mean or sigma since either numbers
            need to be provided or mu and sigma needs to be provided""")

    def calculate_mean(self) -> float:
        """Function to calculate mean"""

        if self.data:
            return np.mean(self.data)
        else:
            return self.mu

    def calculate_std(self) -> float:
        """Function to calculate standard deviation"""

        if self.data:
            return np.std(self.data)
        else:
            return self.sigma

    def read_data_file(self, file_name: str = "") -> None:
        """
        Function to read in data file and then compute
        mean and standard deviation
        """

        if Path(file_name).is_file():
            with open(file_name, "r") as file:
                data_list = []
                line = file.readline()
                while line:
                    data_list.append(int(line))
                    line = file.readline()

            self.data = data_list
            self.mu = self.calculate_mean()
            self.sigma = self.calculate_std()

        else:
            raise FileNotFoundError(f"""{file_name} doesn't exist, please check
            the file or path""")

    def plot_histogram(self) -> None:
        """Function to plot histogram"""

        if self.data:
            plt.hist(self.data)
            plt.title("Histogram of data")
            plt.xlabel("data")
            plt.ylabel("count")
        else:
            raise ValueError("Histogram cannot be generated as no\
                data has been provided")

    def pdf(self, x: float) -> float:
        """Probability density function calculator
           for the gaussian distribution"""

        return (1.0 / (self.sigma * np.sqrt(2*math.pi))) * \
            np.exp(-0.5*((x - self.mu) / self.sigma) ** 2)

    def __add__(self, other):
        """Function to add two gaussians together"""

        result = Gaussian(mu=0, sigma=0)
        result.mu = self.mu + other.mu
        result.sigma = math.sqrt(self.sigma ** 2 + other.sigma ** 2)
        return result

    def __repr__(self):
        """Printing the result in the a long format"""

        return f"mean is {self.mu} and std is {self.sigma}"
