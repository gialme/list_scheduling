"""
Main module for the list scheduling algorithm.
"""

#from list_scheduling.parser import setup_parser, process_file
#from list_scheduling.schedulers import asap_scheduling, alap_scheduling, priority_scheduling
#from list_scheduling.utils import check_same_name

import list_scheduling.parser
import list_scheduling.schedulers
import list_scheduling.utils

def main(args):
    """
    Main function
    """
    array_operations = list_scheduling.parser.process_file(args.file)

    # check for duplicate names among the operations
    duplicate_name = list_scheduling.utils.check_same_name(array_operations)
    if duplicate_name:
        raise ValueError(f"Error. Operation {duplicate_name} has been found twice")

    # print all the operations loaded
    print("Operations loaded from the config file:")
    for operation in array_operations:
        print(str(operation))

    # perform ASAP scheduling and print the vector
    asap_schedule = list_scheduling.schedulers.asap_scheduling(array_operations)
    print("ASAP scheduling: ", asap_schedule)


    # perform ALAP scheduling and print the vector
    alap_schedule = list_scheduling.schedulers.alap_scheduling(array_operations, asap_schedule)
    print("ALAP scheduling: ", alap_schedule)

    # perform List scheduling
    print("List scheduling:")
    list_schedule = list_scheduling.schedulers.priority_scheduling(array_operations, asap_schedule, alap_schedule, args.nmult, args.nadd)

    return list_schedule

if __name__ == "__main__":
    list_scheduled = main(list_scheduling.parser.setup_parser())
    print(list_scheduled)
