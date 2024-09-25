"""
Module for processing configuration file and setting up command-line arguments for the list scheduling algorithm.

Functions:
----------
1. process_file(file_path)

2. setup_parser():
"""

import argparse
from list_scheduling.operation import Operation

def process_file(file_path):
    """
    Parses a configuration file and returns a list of operations.

    The function reads a file line by line, where each line describes a mathematical operation. 
    It ignores comments (lines starting with '#') and empty lines. Each valid line must follow 
    the format: "uX := operand1 operator operand2", where:
    - 'uX' is the name of the operation (must start with 'u'),
    - ':=' is a required delimiter,
    - 'operand1' and 'operand2' are the two operands,
    - 'operator' is one of '+', '-', '*', or '/'.

    Parameters:
    -----------
    file_path : str
        The path to the configuration file to be processed.

    Returns:
    --------
    list[Operation]
        A list of 'Operation' objects created from the valid lines in the file.

    Raises:
    -------
    FileNotFoundError
        If the file cannot be found at the specified path.
    ValueError
        If a line does not conform to the expected format or contains invalid arguments.
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            array_operations = []
            for line_num, line in enumerate(file, start=1):

                # remove leading and trailing whitespace
                line = line.strip()

                # ignore comments and empty lines
                if (line.startswith('#') or not line):
                    continue

                # split the line into parts
                parts = line.split(" ")

                # every line must contain 5 elements:
                if len(parts) > 5:
                    raise ValueError(f"Error in line {line_num}: too many arguments")

                # operations name must starts with letter 'u'
                if not parts[0].startswith("u"):
                    raise ValueError(f"Error in line {line_num}: operation {parts[0]} must start with the letter 'u'")

                # the delimiter between the operation name and the operands must be ":="
                if not parts[1] == ":=":
                    raise ValueError(f"Error in line {line_num}: operation misspelled ")

                # check allowed types of operation
                if (not parts[3] in ['+', '-', '*', '/']):
                    raise ValueError(f"Error in line {line_num}: operation allowed are only + - * /")

                # create a new Operation object
                new_operation = Operation(parts[0], parts[3], parts[2], parts[4])
                if new_operation:
                    array_operations.append(new_operation)

        return array_operations

    except FileNotFoundError as e:
        raise ValueError(f"Error. File {file_path} not found") from e  # Raise error

def setup_parser() -> argparse.Namespace:
    """
    Sets up and parses command-line arguments for the list scheduling algorithm.

    Returns:
    --------
    argparse.Namespace
        A namespace object containing the parsed arguments as attributes.

    Arguments:
    ----------
    - file : str
        The path to the configuration file (required).
    - --nmult : int
        The number of multipliers available for scheduling (required).
    - --nadd : int
        The number of adders available for scheduling (required).
    """
    parser = argparse.ArgumentParser (
        prog='list_scheduling',
        description='Computes the list based scheduling algorithm'
    )

    # argument for the file path
    parser.add_argument("file", type=str, help="path to config file")

    # arguments for numbers of multipliers and adders
    parser.add_argument("--nmult", type=int, help="Number of multipliers available", required=True)
    parser.add_argument("--nadd", type=int, help="Number of adders available", required=True)

    return parser.parse_args()
