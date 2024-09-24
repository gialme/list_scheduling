import argparse
import re

class Operation:
    """
    Represents a mathematical operation involving two operands and a specific operation type.
    """
    def __init__(self, name: str, type: str, input1: str, input2: str):
        """
        Init function.

        Parameters:
        -----------
        _name : str
            The name of the operation. Must be "u<number>" (e.g., 'u0', 'u1', 'u2').
        _type : str
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

        if (type == '+' or type == '-'):
            self._type = "+"
        else:
            self._type = "*"
        
        self._index1 = extract_index(input1)
        self._index2 = extract_index(input2)
    
    # getters
    @property
    def name(self):
        return self._name
    
    @property
    def type(self):
        return self._type
    
    @property
    def input1(self):
        return self._input1
    
    @property
    def input2(self):
        return self._input2
    
    @property
    def index1(self):
        return self._index1
    
    @property
    def index2(self):
        return self._index2
    
    def __str__(self):
        return f"{self.name} := {self.input1} {self.type} {self.input2}"
    
def extract_index(input: str) -> int:
    """
    Extracts the index from an operand string that follows a specific pattern.

    The function expects the input to be in the format "u<number>" (e.g., "u12"). 
    If the input matches this format, the function returns the numerical part of the string as an integer.
    If the input does not match this pattern (e.g., "a"), the function returns -1.

    Parameters:
    -----------
    input : str
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
    match = re.match(pattern, input)

    if match:
        # extract the captured group containing the integer using group(1)
        return int(match.group(1))
    else:
        return -1

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
        with open(file_path, 'r') as file:
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
                if (len(parts) > 5):
                    raise ValueError(f"Error in line {line_num}: too many arguments")
                
                # operations name must starts with letter 'u'
                if (not parts[0].startswith("u")):
                    raise ValueError(f"Error in line {line_num}: operation {parts[0]} must start with the letter 'u'")
                
                # the delimiter between the operation name and the operands must be ":="
                if (not parts[1] == ":="):
                    raise ValueError(f"Error in line {line_num}: operation misspelled ")
                
                # check allowed types of operation
                if (not parts[3] in ['+', '-', '*', '/']):
                    raise ValueError(f"Error in line {line_num}: operation allowed are only + - * /")
                
                # create a new Operation object
                new_operation = Operation(parts[0], parts[3], parts[2], parts[4])
                if new_operation:
                    array_operations.append(new_operation)
        
        return array_operations

    except FileNotFoundError:
        print(f"Error. File {file_path} non found")

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

def check_same_name(objects):
    """
    Checks if any operation name appears more than once in the provided list of objects.

    This function iterates through a list of objects and checks if any two objects share the same name.
    If a duplicate name is found, it returns that name.
    If no duplicates are found, it returns 'False'.

    Parameters:
    -----------
    objects : list
        A list of objects, where each object is expected to have a 'name' attribute.

    Returns:
    --------
    str or bool
        The name of the duplicate operation if found. Returns 'False' if no duplicates are found.
    """
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            if objects[i].name == objects[j].name:
                return objects[i].name
    
    return False

def asap_scheduling(array_operations):
    """
    Performs ASAP (As Soon As Possible) scheduling on a list of operations and returns the clock cycle number in which 
    each operation is performed.

    This function simulates the ASAP scheduling algorithm, which schedules operations as early as possible, 
    taking into account data dependencies. Operations can only be scheduled when their input operands are available 
    (either as inputs or the results of previously scheduled operations).

    Parameters:
    -----------
    array_operations : list[Operation]
        A list of 'Operation' objects, read from the config file, where each operation specifies its dependencies via 'index1' and 'index2'.
        
    Returns:
    --------
    list[int]
        A list of integers where each index represents the clock cycle at which the corresponding operation is scheduled.
        If an operation is scheduled in cycle 'n', the list will contain the value 'n' at that operation's index.

    Example:
    --------
    >>> asap_scheduling(array_operations)
    [1, 1, 2]
    
    This means the first two operations are scheduled in cycle 1, and the third operation is scheduled in cycle 2.
    """
    num_op = len(array_operations)
    # done tracks the clock cycle in wich an operation is performed
    # both arrays are initialized with the value -1 (operation is still waiting)
    done = [-1] * num_op
    temp = [-1] * num_op

    for clk in range(1, num_op+1):
        for i in range(num_op):

            if done[i] != -1: # the operation has already been performed in a previous clk cycle
                continue
            
            # Get the input operand indexes
            index1 = array_operations[i].index1
            index2 = array_operations[i].index2

            # check if both operands are input variable
            # if True, the operation can be done in this clock cycle
            if index1 == -1 and index2 == -1:
                temp[i] = clk
                continue

            # Check if the first operand is available
            if index1 != -1 and done[index1] != -1:
                if index2 != -1 and done[index2] != -1:
                    # both operands are available -> schedule now
                    temp[i] = clk
                    continue
                
                elif index2 == -1:
                    # op1 is done and op2 is an input variable -> scheule now
                    temp[i] = clk
                    continue

            if index1 == -1 and index2 != -1 and done[index2] != -1:
                # op1 is an input variable and op2 is done -> schedule now
                temp[i] = clk
                continue
            
        if done == temp:
            # no changes in the last clk cycle, so break the loop
            clk -= 1
            break

        # update the done array after every clk cycle
        done = temp.copy()
    
    return done

def alap_scheduling(array_operations, asap_schedule):
    """
    Performs ALAP (As Late As Possible) scheduling on a list of operations, based on the given ASAP schedule, 
    and returns the clock cycle number in which each operation is performed.

    ALAP scheduling schedules operations as late as possible while still satisfying data dependencies. 
    It works backwards from the latest operation (determined from the ASAP schedule) and schedules earlier operations 
    based on when their results are needed by dependent operations.

    Parameters:
    -----------
    array_operations : list[Operation]
        A list of 'Operation' objects, where each operation specifies its dependencies via 'index1' and 'index2'.
    
    asap_schedule : list[int]
        The clock cycle numbers from the ASAP scheduling result.

    Returns:
    --------
    list[int]
        A list of integers where each index represents the clock cycle at which the corresponding operation is scheduled in ALAP.
        The list will contain the value 'n' at the operation's index, indicating that the operation is scheduled in cycle 'n'.
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

                # if op1 and op2 are NOT input variable -> schedule the operation now
                if index1 != -1:
                    temp[index1] = clk
                if index2 != -1:
                    temp[index2] = clk

        done = temp.copy()

    return done

def priority_function(asap_schedule, alap_schedule, num_op):
    """
    Computes the scheduling priority for each operation based on the difference between its ALAP and ASAP schedules.

    The priority is established using the formula: (b - t + 1), where:
    - 'b' is the ALAP schedule (the latest clock cycle in which the operation can be performed),
    - 't' is the ASAP schedule (the earliest clock cycle in which the operation can be performed).

    Higher priority values correspond to operations that have a smaller window between their ASAP and ALAP schedules, 
    indicating they should be scheduled earlier.

    Parameters:
    -----------
    asap_schedule : list[int]
        A list of integers representing the clock cycle for each operation in the ASAP scheduling.

    alap_schedule : list[int]
        A list of integers representing the clock cycle for each operation in the ALAP scheduling.

    num_op : int
        The number of the operations.

    Returns:
    --------
    list[int]
        A list of integers representing the priority of each operation. The priority is computed as the difference 
        between the ALAP and ASAP schedules + 1, where smaller differences indicate higher scheduling flexibility.
    """
    priority = [0] * num_op

    # priority is computed as (b-t+1) for each operation
    for i in range(num_op):
        priority[i] = alap_schedule[i] - asap_schedule[i] + 1

    return priority

def priority_scheduling(array_operations, asap_schedule, alap_schedule, n_mult, n_adder):
    """
    Schedules operations based on priority using the Priority Scheduling algorithm, considering both 
    ALAP and ASAP schedules, as well as the number of available adders and multipliers.

    This function implements a priority scheduling mechanism that selects operations to execute based 
    on their priority, which is determined by their ALAP and ASAP schedules. The function prioritizes 
    operations with a smaller window between their ASAP and ALAP schedules and schedules them based on 
    the availability of computational resources (wich are adders and multipliers).
    It also displays on each clock cycle which operations are performed by the assigned number of
    adders and multipliers.

    Parameters:
    -----------
    array_operations : list[Operation]
        A list of 'Operation' objects, which contain information about each operation's dependencies and types.
    
    asap_schedule : list[int]
        A list of integers representing the earliest clock cycles in which each operation can be executed (from the ASAP scheduling).
    
    alap_schedule : list[int]
        A list of integers representing the latest clock cycles in which each operation can be executed (from the ALAP scheduling).
    
    n_mult : int
        The number of multipliers available for scheduling operations (command line argument).
    
    n_adder : int
        The number of adders available for scheduling operations (command line argument).

    Returns:
    --------
    list[int]
        A list of integers where each index corresponds to the clock cycle in which the respective operation is scheduled.
    """
    num_op = len(array_operations)
    
    # init state variables
    ready = [0] * num_op
    temp = [0] * num_op
    scheduling = [-1] * num_op

    add = [-1] * num_op
    mult = [-1] * num_op

    # get operation priorities based on ASAP and ALAP schedules
    priority = priority_function(asap_schedule, alap_schedule, num_op)

    # 'done' and 'temp' vectors have the values:
    # 0 if the corresponding operation is not ready
    # 1 if it's ready but not yet executed
    # 2 if it's executed

    for clk in range(1, num_op + 1):
        for i in range(num_op):
            # search for ready operations in this clk cycle 
            # operation is ready if the inputs are -1 (input variable) or 2 (operands available)
            if ready[i] != 0:
                continue
            
            index1 = array_operations[i].index1
            index2 = array_operations[i].index2

            # check if both operands are input variable (index = -1)
            if index1 == -1 and index2 == -1:
                # if conditions are met, changes its status to ready (1)
                temp[i] = 1
                continue
            
            # check if op1 is done and op2 is either an input variable or done
            if index1 != -1 and ready[index1] == 2:
                if index2 == -1 or (index2 != -1 and ready[index2] == 2):
                    temp[i] = 1
                    continue

            # check if op1 is an input variable and op2 is done
            if index2 != -1 and ready[index2] == 2 and index1 == -1:
                temp[i] = 1
                continue

        ready = temp.copy()

        # print current clock cycle and ready operations
        print("clk: ", clk)
        print("ready operations: ", ready)

        # init adder and multiplier queues
        add = [-1] * n_adder
        mult = [-1] * n_mult

        # assign operations to adders and multipliers based on priority
        # adders
        for i in range(n_adder):
            for j in range(num_op):
                if array_operations[j].type == '+' and ready[j] == 1:
                    if j in add:
                        # operation j is already in the add[] vector, skip
                        continue
                    elif add[i] == -1:
                        # if one adders is empty, assign the operation j
                        add[i] = j
                    elif priority[add[i]] < priority[j]:
                        # if another operation with higher priority is found, replace it
                        add[i] = j
        
        print("adders: ", add)

        # execute additions and mark the corresponding operations as scheduled (2)
        for i in range(n_adder):
            if add[i] != -1:
                temp[add[i]] = 2
                scheduling[add[i]] = clk

        # multipliers
        for i in range(n_mult):
            for j in range(num_op):
                if array_operations[j].type == '*' and ready[j] == 1:
                    if j in mult:
                        continue
                    elif mult[i] == -1:
                        mult[i] = j
                    elif priority[mult[i]] < priority[j]:
                        mult[i] = j

        print("multipliers: ", mult)

        # execute multiplication and mark the corresponding operations as scheduled (2)
        for i in range(n_mult):
            if mult[i] != -1:
                temp[mult[i]] = 2
                scheduling[mult[i]] = clk

        # update the ready[] vector
        ready = temp.copy()

        # check if all operation are marked as done. if true, exit the loop
        if all(x == 2 for x in ready):
            break

    return scheduling

def main():
    """
    Main function
    """
    args = setup_parser()

    array_operations = process_file(args.file)

    # check for duplicate names among the operations
    duplicate_name = check_same_name(array_operations)
    if (duplicate_name):
        raise ValueError(f"Error. Operation {duplicate_name} has been found twice")

    # print all the operations loaded
    print("Operations loaded from the config file:")
    for operation in array_operations:
        print(str(operation))


    # perform ASAP scheduling and print the vector
    asap_schedule = asap_scheduling(array_operations)
    print("ASAP scheduling: ", asap_schedule)


    # perform ALAP scheduling and print the vector
    alap_schedule = alap_scheduling(array_operations, asap_schedule)
    print("ALAP scheduling: ", alap_schedule)

    # perform List scheduling
    print("List scheduling:")
    list_schedule = priority_scheduling(array_operations, asap_schedule, alap_schedule, args.nmult, args.nadd)
    print(list_schedule)

if __name__ == "__main__":
    main()
