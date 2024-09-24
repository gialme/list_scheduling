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