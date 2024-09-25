"""__init__ file of the project"""
from . import list_scheduling

def main():
    """
    main function of __init__ file. It calls the main function in list_scheduling.py
    """
    print(list_scheduling.main(list_scheduling.setup_parser()))
