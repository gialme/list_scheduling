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
                line = line.strip()

                # ignore comments and empty lines
                if (line.startswith('#') or not line):
                    continue

                parts = line.split(" ")

                # every line must contain 5 elements:
                if (len(parts) > 5):
                    raise ValueError(f"Error in line {line_num}: too many arguments")
                
                # operations name must starts with letter 'u'
                if (not parts[0].startswith("u")):
                    raise ValueError(f"Error in line {line_num}: operation {parts[0]} must start with the letter 'u'")
                
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
    
    return False

def asap_scheduling(array_operations):
    """
    returns the clock cycle number in which every operation is performed through an ASAP scheduling
    """
    num_op = len(array_operations)
    # done stores the clock cycle in wich an operation is performed
    # both arrays are initialized with the value -1 (operation is still waiting)
    done = [-1] * num_op
    temp = [-1] * num_op

    for clk in range(1, num_op+1):
        for i in range(num_op):

            if done[i] != -1: # the operation has already been performed in a previous clk cycle
                continue
            
            index1 = array_operations[i].index1
            index2 = array_operations[i].index2

            if index1 == -1 and index2 == -1:
                # both operands are input variabile -> the operation can already be done in this clock cycle
                temp[i] = clk
                continue

            if index1 != -1 and done[index1] != -1:
                if index2 != -1 and done[index2] != -1:
                    # both operands have already been performed -> the operation can be done in this clk cycle
                    temp[i] = clk
                    continue
                
                elif index2 == -1:
                    # op1 is done and op2 is an input variable -> the operation can be done in this clk cycle
                    temp[i] = clk
                    continue

            if index1 == -1 and index2 != -1 and done[index2] != -1:
                # op1 is an input variable and op2 is done -> the operation can be done in this clk cycle
                temp[i] = clk
                continue
            
        if done == temp:
            # no changes in the last clk cycle, i can exit
            clk -= 1
            break

        # update the done array after every clk cycle
        done = temp.copy()
    
    return done

def alap_scheduling(array_operations, asap_schedule):
    """
    returns the clock cycle number in which every operation is performed through an ALAP scheduling
    """
    num_op = len(array_operations)

    # init done array
    done = [-1] * num_op

    # search for the clock max in the asap schedule
    clk_max = max(asap_schedule)
    # search for the index of the last operation in the asap schedule
    pos = asap_schedule.index(clk_max)
    # the last operation in asap is also the last operation in alap
    done[pos] = clk_max

    temp = done.copy()

    # starting from clk-1 and proceed backwards
    for clk in range(clk_max - 1, 0, -1):
        for i in range(num_op):
            if done[i] == clk + 1:
                # pick the the index of the two operands
                index1 = array_operations[i].index1
                index2 = array_operations[i].index2

                # if op1 and op2 are NOT input variable -> schedule them for the current clk cycle
                if index1 != -1:
                    temp[index1] = clk
                if index2 != -1:
                    temp[index2] = clk

        done = temp.copy()

    return done

def priority_function(array_operations, asap_schedule, alap_schedule):
    """
    Establishes the scheduling priority for the operations using the formula (b - t + 1)
    where b: ALAP, t: ASAP
    """
    num_op = len(array_operations)

    priority = [0] * num_op

    for i in range(num_op):
        priority[i] = alap_schedule[i] - asap_schedule[i] + 1

    return priority

def priority_scheduling(array_operations, asap_schedule, alap_schedule, n_mult, n_adder):
    num_op = len(array_operations)
    
    ready = [0] * num_op
    temp = [0] * num_op
    scheduling = [-1] * num_op
    all_done = [2] * num_op

    add = [-1] * num_op
    mult = [-1] * num_op

    # call the priority function
    priority = priority_function(array_operations, asap_schedule, alap_schedule)

    # done and temp vectors have the values:
    # 0 if the corresponding operation is not ready
    # 1 if it's ready but not yet executed
    # 2 if it's executed

    for clk in range(1, num_op + 1):
        for i in range(num_op):
            # search for ready operations for this clk cycle 
            # operation is ready if the inputs are -1 (input variable) or 2
            if ready[i] != 0:
                continue
            
            index1 = array_operations[i].index1
            index2 = array_operations[i].index2

            if index1 == -1 and index2 == -1:
                # if conditions are met, changes its status in ready (1)
                temp[i] = 1
                continue
            
            if index1 != 1 and ready[index1] == 2:
                if index2 == -1 or (index2 != -1 and ready[index2] == 2):
                    temp[i] = 1
                    continue

            if index2 != -1 and ready[index2] == 2 and index1 == -1:
                temp[i] = 1
                continue

        ready = temp.copy()

        print("clk: ", clk)
        print("ready operations: ", ready)

        # init adder and multiplier queues
        add = [-1] * n_adder
        mult = [-1] * n_mult

        # search for ready additions and put them in the add[] vector
        for i in range(n_adder):
            for j in range(num_op):
                if array_operations[j].type == '+' and ready[j] == 1:
                    if j in add:
                        # operation is already in the add[] vector, skip
                        continue
                    elif add[i] == -1:
                        add[i] = j
                    elif priority[add[i]] < priority[j]:
                        # if another operation with higher priority is found, replace it
                        add[i] = j
        
        print("adder: ", add)

        # execute additions and update the done[] vector
        for i in range(n_adder):
            if add[i] != -1:
                temp[add[i]] = 2
                scheduling[add[i]] = clk

        # search for ready multiplications
        for i in range(n_mult):
            for j in range(num_op):
                if array_operations[j].type == '*' and ready[j] == 1:
                    if j in mult:
                        continue
                    elif mult[i] == -1:
                        mult[i] = j
                    elif priority[mult[i]] < priority[j]:
                        mult[i] = j

        print("multiplier: ", mult)

        # execute multiplication and update the done[] vector
        for i in range(n_mult):
            if mult[i] != -1:
                temp[mult[i]] = 2
                scheduling[mult[i]] = clk

        # update the ready[] vector
        ready = temp.copy()

        # check if all operation are done. if true, exit the loop
        if all(x == 2 for x in ready):
            break

    return scheduling


if __name__ == "__main__":
    args = setup_parser()

    array_operations = process_file(args.file)

    duplicate_name = check_same_name(array_operations)

    if (duplicate_name):
        raise ValueError(f"Error. Operation {duplicate_name} has been found twice")

    print("Operations loaded from the config file:")
    for operation in array_operations:
        print(str(operation))

    asap_schedule = asap_scheduling(array_operations)

    print("ASAP scheduling: ", asap_schedule)

    alap_schedule = alap_scheduling(array_operations, asap_schedule)

    print("ALAP scheduling: ", alap_schedule)

    print("List scheduling:")
    list_schedule = priority_scheduling(array_operations, asap_schedule, alap_schedule, args.nmult, args.nadd)
