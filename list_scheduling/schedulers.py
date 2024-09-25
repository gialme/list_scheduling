"""
This module provides functions for scheduling operations using ASAP, ALAP, and priority-based
scheduling algorithms.

Functions:
----------
- asap_scheduling(array_operations): 
    Performs ASAP scheduling by determining the earliest time an operation can be scheduled based on its dependencies.
    
- alap_scheduling(array_operations, asap_schedule): 
    Performs ALAP scheduling by determining the latest time an operation can be scheduled without violating dependencies.
    
- priority_scheduling(array_operations, asap_schedule, alap_schedule, n_mult, n_adder): 
    Schedules operations based on priority using the Priority Scheduling algorithm, considering the results from ASAP 
    and ALAP scheduling, as well as the number of available computational resources (adders and multipliers).

Helper Functions:
-----------------
- priority_function(asap_schedule, alap_schedule, num_op): 
    A utility function used in priority scheduling to determine the priority of each operation based on the window
    between ASAP and ALAP schedules.
"""
from list_scheduling.utils import priority_function

def asap_scheduling(array_operations):
    """
    Performs ASAP (As Soon As Possible) scheduling on a list of operations and returns the clock cycle number in which 
    each operation is performed.

    This function simulates the ASAP scheduling algorithm, which schedules operations as early as possible, 
    taking into account data dependencies. Operations can only be scheduled when their input operands are available 
    (either as inputs or the results of previously scheduled operations).

    Parameters:
    -----------
    array_operations : list[ScheduleOperation]
        A list of 'ScheduleOperation' objects, read from the config file, where each operation specifies its dependencies via 'index1' and 'index2'.
        
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

                if index2 == -1:
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
    array_operations : list[ScheduleOperation]
        A list of 'cheduleOperation' objects, where each operation specifies its dependencies via 'index1' and 'index2'.
    
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
    array_operations : list[ScheduleOperation]
        A list of 'ScheduleOperation' objects, which contain information about each operation's dependencies and types.
    
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
                if array_operations[j].type_op == '+' and ready[j] == 1:
                    if j in add:
                        # operation j is already in the add[] vector, skip
                        continue
                    if add[i] == -1:
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
                if array_operations[j].type_op == '*' and ready[j] == 1:
                    if j in mult:
                        continue
                    if mult[i] == -1:
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
