from pathlib import Path


class Distribution():
    """A package to calculate gaussian distribution and probabilities"""
    def __init__(self, mu: float = None, sigma: float = None) -> None:

        self.mu = mu
        self.sigma = sigma
        self.data = []

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
