import pytest
import tempfile
import os
import sys
import list_scheduling.list_scheduling
import list_scheduling.parser

@pytest.fixture
def temp_config_file():
    """
    Create a temporary configuration file for testing purposes
    """
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
        f.write("u0 := a + b\n")
        f.write("u1 := c - d\n")
        f.write("u2 := u1 * e\n")
        f.write("u3 := u2 / u0\n")
        temp_file_name = f.name
    yield temp_file_name
    # remove the temporary file
    os.remove(temp_file_name)

class TestIntegration:
    def test_integration(self, temp_config_file):
        """
        Integration test for the list scheduling algorithm
        """
        array_operations = list_scheduling.parser.process_file(temp_config_file)

        # perform asap scheduling
        asap_schedule = list_scheduling.schedulers.asap_scheduling(array_operations)
        assert asap_schedule == [1, 1, 2, 3]

        # perform alap scheduling
        alap_schedule = list_scheduling.schedulers.alap_scheduling(array_operations, asap_schedule)
        assert alap_schedule == [2, 1, 2, 3]

        # perform priority scheduling (nadd=2, nmult=2)
        list_schedule = list_scheduling.schedulers.priority_scheduling(array_operations, asap_schedule, alap_schedule, 2, 2)
        assert list_schedule == [1, 1, 2, 3]
    
    def test_integration_duplicate(self, monkeypatch):
        """
        This test should raise a ValueError due to a duplicate operation name
        """
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("u0 := a + b\n")
            f.write("u0 := c - d\n")
            f.write("u2 := u0 * e\n")
            f.write("u3 := u2 / u0\n")
            temp_file_name = f.name

        try:
            test_args = ["list_scheduling", temp_file_name, "--nmult", "2", "--nadd", "2"]

            monkeypatch.setattr(sys, 'argv', test_args)

            with pytest.raises(ValueError, match="Error. Operation u0 has been found twice"):
                args = list_scheduling.parser.setup_parser()
                list_scheduling.list_scheduling.main(args)
        finally:
            os.remove(temp_file_name)