"""
This module contains the Operation class, which represents a mathematical operation involving two operands
and a specific operation type. The module also includes a utility function to extract the index from an operand string.
"""
import re

class ScheduleOperation:
    """
    Represents a mathematical operation involving two operands and a specific operation type.
    """
    def __init__(self, name: str, type_op: str, input1: str, input2: str):
        """
        Init function.

        Parameters:
        -----------
        _name : str
            The name of the operation. Must be "u<number>" (e.g., 'u0', 'u1', 'u2').
        _type_op : str
            The type of the elementary operation, represented as either '+' or '*' 
            based on whether the operation is an addition/subtraction or multiplication/division. 
            If the operation is '+' or '-', the type is set to '+' (adder).
            If the operation is '*' or '/', the type is set to '*' (multiplier).
        _input1 : str
            The first operand for the operation, which could be an input variable or a previous operation.
        _input2 : str
            The second operand for the operation, which could be an input variable or a previous operation.
        _index1 : int
            The index of the first operand, extracted from 'input1'. If it is an input variable, the index is set to -1.
        _index2 : int
            The index of the second operand, extracted from 'input2'. If it is an input variable, the index is set to -1.
        """
        self._name = name
        self._input1 = input1
        self._input2 = input2

        if (type_op in ('+', '-')):
            self._type_op = "+"
        else:
            self._type_op = "*"

        self._index1 = extract_index(input1)
        self._index2 = extract_index(input2)

    # getters
    @property
    def name(self):
        """Gets the name of the operation."""
        return self._name

    @property
    def type_op(self):
        """Gets the type of the operation (+ for adder, * for multiplier)."""
        return self._type_op

    @property
    def input1(self):
        """Gets the first operand of the operation."""
        return self._input1

    @property
    def input2(self):
        """Gets the second operand of the operation."""
        return self._input2

    @property
    def index1(self):
        """Gets the index of the first operand (or -1 if it is an input variable)."""
        return self._index1

    @property
    def index2(self):
        """Gets the index of the second operand (or -1 if it is an input variable)."""
        return self._index2

    def __str__(self):
        """Returns a string representation of the operation."""
        return f"{self.name} := {self.input1} {self.type_op} {self.input2}"

def extract_index(operand: str) -> int:
    """
    Extracts the index from an operand string that follows a specific pattern.

    The function expects the input to be in the format "u<number>" (e.g., "u12"). 
    If the input matches this format, the function returns the numerical part of the string as an integer.
    If the input does not match this pattern (e.g., "a"), the function returns -1.

    Parameters:
    -----------
    operand : str
        The operand string from which the index is to be extracted. 
        It is expected to be in the format "u<number>".

    Returns:
    --------
    int
        The extracted numerical index if the input matches the pattern. 
        Returns -1 if the input does not match the pattern.
    """

    # regular expression pattern to match the expected format
    pattern = r"^u(\d+)$"
    match = re.match(pattern, operand)

    if match:
        # extract the captured group containing the integer using group(1)
        return int(match.group(1))

    return -1
