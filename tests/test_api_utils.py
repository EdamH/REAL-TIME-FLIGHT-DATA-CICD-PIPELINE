import os
import pytest
from unittest.mock import patch, mock_open
# Modify the path to include the parent directory
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.api_utils import export_data_to_json, get_data, format_data

# Mock environment variables
os.environ['flights_api_url'] = 'http://mockapi.com/'
os.environ['flights_api_key'] = 'mockapikey'


# Mock response data
mock_data = [{'lat': 10, 'lng': 20, 'other_field': 'value'}]

@patch('utils.api_utils.requests.get')
def test_get_data(mock_get):
    mock_get.return_value.json.return_value = {"response": mock_data}
    endpoint = 'mockendpoint'
    params = {'_fields': 'lat,lng,other_field'}
    response = get_data(endpoint, **params)
    assert response == mock_data

def test_format_data():
    formatted_data = format_data(mock_data)
    expected_data = [{'position': {'lat': 10, 'lon': 20}, 'other_field': 'value'}]
    assert formatted_data == expected_data

@patch('utils.api_utils.get_data')
@patch('utils.api_utils.open', new_callable=mock_open)
def test_export_data_to_json(mock_open, mock_get_data):
    mock_get_data.return_value = mock_data
    endpoint = 'mockendpoint'
    fields = 'lat,lng,other_field'
    filename = 'test_data.json'
    export_data_to_json(endpoint, fields, filename)
    mock_open.assert_called_once_with(f'utils/{filename}', 'w')

@pytest.fixture(autouse=True)
def run_around_tests():
    # Clean up any test artifacts before/after running tests
    yield
    if os.path.exists('utils/test_data.json'):
        os.remove('utils/test_data.json')
