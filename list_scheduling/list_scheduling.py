import argparse


# class Operation is defined with:
# name: operation name (eg. u0, u1, u2)
# type: +, -, *, /
# input1, input2: the two operand
# index1, index2: their index (-1 if it's an input variable)
class Operation:
    def __init__(self, name: str, type: str, input1: str, input2: str, index1: int, index2: int):
        self._name = name
        self._type = type
        self._input1 = input1
        self._input2 = input2
        self._index1 = index1
        self._index2 = index2
    
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

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"File read: \n{content}")
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
    
    args = parser.parse_args()

    process_file(args.file)

if __name__ == "__main__":
    setup_parser()