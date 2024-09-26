from hypothesis import given, settings, strategies as st
from list_scheduling.utils import priority_function

@st.composite
def schedules_and_num_op(draw):
    """
    Strategy to generate a list of schedules and num_op
    num_op can't be greater than the length of the schedule, otherwise it will raise an out of index error
    """
    schedule=draw(st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=100))
    num_op=draw(st.integers(min_value=1, max_value=len(schedule)))
    return schedule, num_op

class TestProperty:

    @given(schedules_and_num_op())
    @settings(max_examples=100)
    def test_priority_function_length(self, schedules_and_num_op):
        """
        Test the priority function making sure the lengths of the vectors match num_op
        """
        schedule, num_op = schedules_and_num_op
        # the length of the vector schedule must be equal to num_op
        schedule = schedule[:num_op]
        print(schedule)

        # feeding priority function with the same schedule twice, since i only need to check its return length
        priority = priority_function(schedule, schedule, num_op)

        assert len(priority) == num_op
    
    @given(schedules_and_num_op())
    @settings(max_examples=100)
    def test_priority_function_type(self, schedules_and_num_op):
        """
        Test the priority function making sure the return type is a list of integers
        """
        schedule, num_op = schedules_and_num_op
        
        priority = priority_function(schedule, schedule, num_op)

        assert all(isinstance(x, int) for x in priority)
