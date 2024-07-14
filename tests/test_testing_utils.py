import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open

# Modify the path to include the parent directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.testing_utils import testing_module


@pytest.fixture
def producer():
    producer = MagicMock()
    return producer

@pytest.fixture
def temp_json_file():
    data = [
        {"message": "test1"},
        {"message": "test2"},
        {"message": "test3"}
    ]
    return json.dumps(data)
    

def test_testing_module(producer, temp_json_file):
    # Call the function with the mock producer and check if it behaves as expected
    # Mock the os.path.exists to return True
    with patch('os.path.exists', return_value=True):
        # Mock the open function to read the sample_data
        with patch('builtins.open', mock_open(read_data=temp_json_file)):
            # Patch time.sleep to speed up the test
            with patch('time.sleep', return_value=None):
                testing_module(producer, temp_json_file)
                print('done')

    # Check that the producer's send method was called the correct number of times
    assert producer.send.call_count == 3

    # Check that the messages sent are correct
    expected_calls = [
        {"message": "test1"},
        {"message": "test2"},
        {"message": "test3"}
    ]
    actual_calls = [call[0][1] for call in producer.send.call_args_list]
    assert actual_calls == expected_calls

    # Check that producer.flush was called once
    producer.flush.assert_called_once()
