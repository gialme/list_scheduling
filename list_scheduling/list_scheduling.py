"""
Main module for the list scheduling algorithm.
"""

from list_scheduling.parser import setup_parser, process_file
from list_scheduling.schedulers import asap_scheduling, alap_scheduling, priority_scheduling
from list_scheduling.utils import check_same_name

def main(args):
    """
    Main function
    """
    array_operations = process_file(args.file)

    # check for duplicate names among the operations
    duplicate_name = check_same_name(array_operations)
    if duplicate_name:
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

    return list_schedule

if __name__ == "__main__":
    list_scheduled = main(setup_parser())
    print(list_scheduled)
