import pickle
from .solver import SuPySolver


def load_superset(filename: str):
    """
    Saves the superset instance as a serialized pickle file.

    :param      filename:  The filename
    :type       filename:  str
    """
    with open(f"{filename}.instance.pickle", 'rb') as input_file:
        superset = pickle.load(input_file)

    return superset

# -
