import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Modify the path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the function to be tested
from utils.kafka_utils import stream_single_flight

# Mock data to be returned by the get_data and format_data functions
mock_data = [{'lat': 10, 'lng': 20, 'other_field': 'value'}]
formatted_data = [{'position': {'lat': 10, 'lon': 20}, 'other_field': 'value'}]

@pytest.fixture
def producer():
    return MagicMock()

def test_stream_single_flight(producer):
    # Mock the necessary functions
    with patch('utils.kafka_utils.get_data', return_value=mock_data) as mock_get_data:
        with patch('utils.kafka_utils.format_data', return_value=formatted_data) as mock_format_data:
            with patch('time.sleep', return_value=None):
                # Call the function with mocked components
                endpoint = 'mockendpoint'
                fields = 'lat,lng,other_field'
                
                stream_single_flight(endpoint, fields, producer, interval=0.1)

    # Check that get_data was called correctly
    mock_get_data.assert_called_once_with(endpoint, _fields=fields)
    
    # Check that format_data was called with the correct data
    mock_format_data.assert_called_once_with(mock_data)
    
    # Check that producer.send was called with the correct data
    assert producer.send.call_count == len(formatted_data)
    for obj in formatted_data:
        producer.send.assert_any_call('flight', obj)
    
    # Check that producer.flush was called once
    producer.flush.assert_called_once()
