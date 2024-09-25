import pytest
import list_scheduling.utils
import list_scheduling.operation
import list_scheduling.schedulers

@pytest.fixture
def operations():
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

class TestUnit:
    @pytest.mark.parametrize("asap, alap, num_op, result", [
        ([1, 1, 2, 3, 3, 4], [1, 2, 2, 3, 3, 4], 6, [1, 2, 1, 1, 1, 1]),
        ([1, 2, 2, 3, 4, 5], [1, 2, 3, 4, 4, 5], 6, [1, 1, 2, 2, 1, 1]),
        ([1, 1, 2, 3, 4, 5], [1, 2, 3, 4, 4, 5], 6, [1, 2, 2, 2, 1, 1])
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

