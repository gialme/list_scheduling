"""__init__ file of the project"""
from . import list_scheduling
from . import parser

def main():
    """
    main function of __init__ file. It calls the main function in list_scheduling.py
    """
    print(list_scheduling.main(parser.setup_parser()))
