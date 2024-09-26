import pytest
import tempfile
import os
import sys
import argparse
import list_scheduling.utils
import list_scheduling.operation
import list_scheduling.schedulers
import list_scheduling.parser
import list_scheduling.list_scheduling

@pytest.fixture
def operations():
    """
    Create a list of ScheduleOperation objects for testing purposes.
    """
    return [
        list_scheduling.operation.ScheduleOperation('u0', '+', 'a', 'b'), # Operation 0: No dependencies
        list_scheduling.operation.ScheduleOperation('u1', '*', 'c', 'd'), # Operation 1: No dependencies
        list_scheduling.operation.ScheduleOperation('u2', '*', 'e', 'f'), # Operation 2: No dependencies
        list_scheduling.operation.ScheduleOperation('u3', '*', 'g', 'h'), # Operation 3: No dependencies
        list_scheduling.operation.ScheduleOperation('u4', '+', 'u0', 'u1'),# Operation 4: Depends on Operations 0 and 1
        list_scheduling.operation.ScheduleOperation('u5', '+', 'u3', 'i'), # Operation 5: Depends on Operations 3
        list_scheduling.operation.ScheduleOperation('u6', '*', 'u4', 'j'), # Operation 6: Depends on Operation 4
        list_scheduling.operation.ScheduleOperation('u7', '*', 'u6', 'u2'),# Operation 7: Depends on Operations 2 and 6
        list_scheduling.operation.ScheduleOperation('u8', '*', 'u7', 'u5') # Operation 8: Depends on Operations 5 and 7
    ]

class TestUnitUtils:
    @pytest.mark.parametrize("asap, alap, num_op, result", [
        ([1, 1, 2, 3, 3, 4], [1, 2, 2, 3, 3, 4], 6, [1, 2, 1, 1, 1, 1]),
        ([1, 2, 2, 3, 4, 5], [1, 2, 3, 4, 4, 5], 6, [1, 1, 2, 2, 1, 1]),
        ([1, 1, 2, 3, 4, 5], [1, 2, 3, 4, 4, 5], 6, [1, 2, 2, 2, 1, 1]),
        ([1, 1, 1, 1, 2, 2, 3, 4, 5], [1, 1, 3, 3, 2, 4, 3, 4, 5], 9, [1, 1, 3, 3, 1, 3, 1, 1, 1]),
        ([1, 1, 1, 2, 2, 3, 3, 4, 5], [1, 1, 3, 3, 2, 4, 3, 4, 5], 9, [1, 1, 3, 2, 1, 2, 1, 1, 1])
        ])
    def test_priority_function(self, asap, alap, num_op, result):
        """
        Test the priority function with parametrization.
        Priority = alap - asap + 1
        """
        #asap = [1, 1, 2, 3, 3, 4]
        #alap = [1, 2, 2, 3, 3, 4]
        #num_op = len(asap)
        #expected_priority = [1, 2, 1, 1, 1, 1]

        priority = list_scheduling.utils.priority_function(asap, alap, num_op)

        assert priority == result

    def test_check_same_name_true(self):
        """
        Test the check_same_name function with two operations with the same name.
        """
        op1 = list_scheduling.operation.ScheduleOperation("u0", "+", "a", "b")
        op2 = list_scheduling.operation.ScheduleOperation("u0", "+", "c", "d")
        expected_res = "u0"

        vector = [op1, op2]

        res = list_scheduling.utils.check_same_name(vector)

        assert res == expected_res
    
    def test_check_same_name_false(self):
        """
        Test the check_same_name function with two operations with different names
        (must return 'False').
        """
        op1 = list_scheduling.operation.ScheduleOperation("u0", "+", "a", "b")
        op2 = list_scheduling.operation.ScheduleOperation("u1", "+", "c", "d")
        
        vector = [op1, op2]

        res = list_scheduling.utils.check_same_name(vector)

        assert res == False

    def test_str_ScheduleOperation(self):
        """
        Test the __str__ method of the ScheduleOperation class.
        """
        operation = list_scheduling.operation.ScheduleOperation("u0", "+", "a", "b")
        expected_str = "u0 := a + b"

        res = str(operation)

        assert res == expected_str

class TestUnitSchedulers:
    """
    Test the scheduling functions.
    """
    #@pytest.mark.skip(reason="skip for now")
    @pytest.mark.usefixtures("operations")
    def test_asap_scheduling(self, operations):
        expected_asap = [1, 1, 1, 1, 2, 2, 3, 4, 5]

        result = list_scheduling.schedulers.asap_scheduling(operations)

        assert result == expected_asap

    @pytest.mark.usefixtures("operations")
    def test_alap_scheduling(self, operations):
        asap = [1, 1, 1, 1, 2, 2, 3, 4, 5]
        expected_alap = [1, 1, 3, 3, 2, 4, 3, 4, 5]

        result = list_scheduling.schedulers.alap_scheduling(operations, asap)

        assert result == expected_alap
    
    @pytest.mark.usefixtures("operations")
    def test_priority_scheduling(self, operations):
        asap = [1, 1, 1, 1, 2, 2, 3, 4, 5]
        alap = [1, 1, 3, 3, 2, 4, 3, 4, 5]
        n_mult = 2
        n_add = 2

        expected_priority_schedule = [1, 2, 1, 1, 3, 2, 4, 5, 6]

        result = list_scheduling.schedulers.priority_scheduling(operations, asap, alap, n_mult, n_add)

        assert result == expected_priority_schedule

class TestParser:
    def test_process_file_valid(self):
        """
        Test the process_file function with a valid file.
        """
        # create a temporary file with valid operations
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write("# this comment should be ignored\n")
            temp_file.write("u0 := a + b\n")
            temp_file.write("u1 := c * d\n")
            temp_file.write("u2 := e - f\n")
            temp_file.write("u3 := u0 / u1\n")
            temp_file_path = temp_file.name
        
        try:
            operations_read = list_scheduling.parser.process_file(temp_file_path)

            expected_operations = [
                list_scheduling.operation.ScheduleOperation('u0', '+', 'a', 'b'),
                list_scheduling.operation.ScheduleOperation('u1', '*', 'c', 'd'),
                list_scheduling.operation.ScheduleOperation('u2', '+', 'e', 'f'), # '-' conveerted to '+'
                list_scheduling.operation.ScheduleOperation('u3', '*', 'u0', 'u1') # '/' converted to '*'
            ]

            # assertions
            assert len(operations_read) == len(expected_operations)
            for i in range(len(operations_read)):
                assert operations_read[i].name == expected_operations[i].name
                assert operations_read[i].type_op == expected_operations[i].type_op
                assert operations_read[i].input1 == expected_operations[i].input1
                assert operations_read[i].input2 == expected_operations[i].input2
        
        finally:
            os.remove(temp_file_path)

    def test_process_file_invalid_arguments(self):
        """
        Test the process_file function with an invalid file where the number of arguments is not 5.
        """
        # create a temporary file exceeding the max number of arguments (5)
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write("u0 := a + b * c\n")
            temp_file_path = temp_file.name

        try:
            # calling the function should raise a ValueError
            with pytest.raises(ValueError, match="Error in line 1: operation misspelled"):
                list_scheduling.parser.process_file(temp_file_path)
        finally:
            os.remove(temp_file_path)
    
    def test_process_file_invalid_operation(self):
        """
        Test the process_file function with an invalid operation name
        where the operation name is invalid (must start with 'u').
        """
        # create a temporary file with an invalid operation
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write("a0 := a + b\n")
            temp_file_path = temp_file.name
        
        try:
            # calling the function should raise a ValueError
            with pytest.raises(ValueError, match="Error in line 1: operation a0 must start with the letter 'u'"):
                list_scheduling.parser.process_file(temp_file_path)
        finally:
            os.remove(temp_file_path)
    
    def test_process_file_invalid_delimiter(self):
        """
        Test the process_file function with an invalid operation
        where the delimiter between the operation name and operands is invalid.
        """
        # create a temporary file with an invalid operation
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write("u0 = a + b\n")
            temp_file_path = temp_file.name
        
        try:
            # calling the function should raise a ValueError
            with pytest.raises(ValueError, match="Error in line 1: operation misspelled"):
                list_scheduling.parser.process_file(temp_file_path)
        finally:
            os.remove(temp_file_path)

    def test_process_file_invalid_operation_type(self):
        """
        Test the process_file function with an invalid operation
        where the operation type is invalid (must be '+', '-', '*', '/').
        """
        # create a temporary file with an invalid operation
        with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write("u0 := a x b\n")
            temp_file_path = temp_file.name
        
        try:
            # calling the function should raise a ValueError
            with pytest.raises(ValueError, match=r"Error in line 1: operation allowed are only \+ - \* /"):
                list_scheduling.parser.process_file(temp_file_path)
        finally:
            os.remove(temp_file_path)
    def test_process_file_file_not_found(self):
        """
        Test the process_file function with a file that does not exist.
        """
        # calling the function should raise a ValueError
        with pytest.raises(ValueError, match="Error. File file_not_existent.txt not found"):
            list_scheduling.parser.process_file("file_not_existent.txt")

    def test_setup_parser_valid(self, monkeypatch):
        """
        Test the setup_parser function simulating command-line arguments.
        """
        # simulate command-line arguments
        test_args = ["list_scheduling", "config.txt", "--nmult", "2", "--nadd", "2"]
        
        # temporarily replace sys.argv with test_args for testing purposes
        # sys.argv usually contains the command-line arguments passed to the script
        monkeypatch.setattr(sys, 'argv', test_args)

        # call the setup_parser function
        args = list_scheduling.parser.setup_parser()

        assert args.file == "config.txt"
        assert args.nmult == 2
        assert args.nadd == 2

class TestListScheduling:
    @pytest.fixture
    def mock_setup_parser(self, monkeypatch):
        def mock_parser():
            return argparse.Namespace(file="config.txt", nmult=2, nadd=2)
        monkeypatch.setattr(list_scheduling.parser, 'setup_parser', mock_parser)

    @pytest.fixture
    def mock_process_file(self, monkeypatch):
        def mock_process(file):
            return [
                list_scheduling.operation.ScheduleOperation('u0', '+', 'a', 'b'),
                list_scheduling.operation.ScheduleOperation('u1', '*', 'c', 'd'),
                list_scheduling.operation.ScheduleOperation('u2', '+', 'u0', 'e'),
                list_scheduling.operation.ScheduleOperation('u3', '*', 'u1', 'u2')
            ]
        monkeypatch.setattr(list_scheduling.parser, 'process_file', mock_process)
    
    @pytest.fixture
    def mock_check_same_name(self, monkeypatch):
        def mock_check(operations):
            return False
        monkeypatch.setattr(list_scheduling.utils, 'check_same_name', mock_check)
    
    @pytest.fixture
    def mock_asap_scheduling(self, monkeypatch):
        def mock_asap(operations):
            return [1, 1, 2, 3]
        monkeypatch.setattr(list_scheduling.schedulers, 'asap_scheduling', mock_asap)
    
    @pytest.fixture
    def mock_alap_scheduling(self, monkeypatch):
        def mock_alap(operations, asap_schedule):
            return [1, 2, 2, 3]
        monkeypatch.setattr(list_scheduling.schedulers, 'alap_scheduling', mock_alap)
    
    @pytest.fixture
    def mock_priority_scheduling(self, monkeypatch):
        def mock_priority(operations, asap_schedule, alap_schedule, n_mult, n_add):
            return [1, 1, 2, 3]
        monkeypatch.setattr(list_scheduling.schedulers, 'priority_scheduling', mock_priority)

    #@pytest.mark.skip(reason="skip for now")
    def test_main_valid_input(self, mock_priority_scheduling, mock_alap_scheduling, mock_asap_scheduling, mock_check_same_name, mock_process_file, mock_setup_parser):
        """
        Test the main function with valid input.
        """
        # call the main function
        args = list_scheduling.parser.setup_parser()
        res = list_scheduling.list_scheduling.main(args)

        assert res == [1, 1, 2, 3]
    
    @pytest.fixture
    def mock_check_same_name_true(self, monkeypatch):
        def mock_check(operations):
            return "u0"
        monkeypatch.setattr(list_scheduling.utils, 'check_same_name', mock_check)
    
    def test_main_duplicate(self, mock_check_same_name_true, mock_priority_scheduling, mock_alap_scheduling, mock_asap_scheduling, mock_process_file, mock_setup_parser):
        """
        Test the main function with duplicate operation names.
        It should raise a ValueError.
        """
        with pytest.raises(ValueError, match="Error. Operation u0 has been found twice"):
            args = list_scheduling.parser.setup_parser()
            list_scheduling.list_scheduling.main(args)