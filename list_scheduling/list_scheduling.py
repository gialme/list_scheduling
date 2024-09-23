import argparse
import re


# class Operation is defined with:
# name: operation name (eg. u0, u1, u2)
# type: +, -, *, /
# input1, input2: the two operands
# index1, index2: their index (-1 if it's an input variable)
class Operation:
    def __init__(self, name: str, type: str, input1: str, input2: str):
        self._name = name
        self._input1 = input1
        self._input2 = input2

        # if the type of operation is + or - -> adder
        # else if the type is * or / -> multiplier
        if (type == '+' or type == '-'):
            self._type = "+"
        else:
            self._type = "*"
        
        self._index1 = extract_index(input1)
        self._index2 = extract_index(input2)
    
    # getters and setters
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name:str):
        self._name = name
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, type:str):
        self._type = type
    
    @property
    def input1(self):
        return self._input1
    
    @input1.setter
    def input1(self, input1:str):
        self._input1 = input1
    
    @property
    def input2(self):
        return self._input2
    
    @input2.setter
    def input2(self, input2:str):
        self._input2 = input2
    
    @property
    def index1(self):
        return self._index1
    
    @index1.setter
    def index1(self, index1:int):
        self._index1 = index1
    
    @property
    def index2(self):
        return self._index2
    
    @index2.setter
    def index2(self, index2:int):
        self._index2 = index2
    
    def __str__(self):
        return f"{self.name} := {self.input1} {self.type} {self.input2}"
    
def extract_index(input: str) -> int:
    """
    Exctracts the index from an operand
    """
    pattern = r"^u(\d+)$"
    match = re.match(pattern, input)

    # if the input is "u12" the index is 12, else (eg. the input is "a") its is index -1
    if match:
        return int(match.group(1))
    else:
        return -1

def process_file(file_path):
    """
    Parses the config file and returns an array with all the operations read from the file
    """
    try:
        with open(file_path, 'r') as file:
            array_operations = []
            for line_num, line in enumerate(file, start=1):

                # remove leading and trailing whitespace
                line.strip()

                # ignore comments and empty lines
                if (line.startswith('#') or not line):
                    continue

                parts = line.split(" ")

                # every line must contain 5 elements:
                if (len(parts) != 5):
                    raise ValueError(f"Error in line {line_num}: too many arguments")
                
                # operations name must starts with letter 'u'
                if (not parts[0].startswith("u")):
                    raise ValueError(f"Error in line {line_num}: operation {parts[0]} must start with the letter 'u")
                
                if (not parts[1] == ":="):
                    raise ValueError(f"Error in line {line_num}: operation misspelled ")
                
                # check allowed types of operation
                if (not parts[3] in ['+', '-', '*', '/']):
                    raise ValueError(f"Error in line {line_num}: operation allowed are only + - * /")

                new_operation = Operation(parts[0], parts[3], parts[2], parts[4])

                if new_operation:
                    array_operations.append(new_operation)
        
        return array_operations

    except FileNotFoundError:
        print(f"Error: {file_path} does not exists")

def setup_parser() -> argparse.Namespace:
    """
    Parses the arguments
    """
    parser = argparse.ArgumentParser (
        prog='list_scheduling',
        description='Computes the list based scheduling algorithm'
    )

    # argument for the file path
    parser.add_argument("file", type=str, help="path to config file")

    # arguments for numbers of multipliers and adders
    parser.add_argument("--nmult", type=int, help="Number of multipliers available")
    parser.add_argument("--nadd", type=int, help="Number of adders available")
    
    return parser.parse_args()

def check_same_name(objects) -> str:
    """
    Checks if an operation name (u0) has been entered twice and if true, returns the name
    """
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if objects[i].name == objects[j].name:
                return objects[i].name
    
    return True

if __name__ == "__main__":
    args = setup_parser()

    array_operations = process_file(args.file)

    print("Operations loaded from the config file:")
    for operation in array_operations:
        print(str(operation))

    duplicate_name = check_same_name(array_operations)

    if (duplicate_name):
        raise ValueError(f"Error. Operation {duplicate_name} has been found twice")