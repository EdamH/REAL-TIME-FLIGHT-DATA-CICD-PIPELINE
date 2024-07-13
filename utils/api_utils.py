from dotenv import load_dotenv
import os
import requests 
import json

# Load environment variables from .env file
load_dotenv()

# Load API variables
api_url = os.environ.get('flights_api_url')
api_key = os.environ.get('flights_api_key')



def export_data_to_json(endpoint, fields, filename='dummy_data.json'):
    """
    Export data to a JSON file.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        fields (dict): Fields to fetch from API.
        filename (str): The name of the file to export the data to.

    """
    file_path = f'utils/{filename}'

    # Check if file exists and remove it if so
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed existing file: {filename}")

    # Fetch data from API
    data = get_data(endpoint, _fields=fields)
    data = format_data(data)

    # Write data to JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print(f"Exported data to {filename}")

# Function to get data from the API
def get_data(endpoint, **params):
    """
    Get data from the API.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        **params: Additional query parameters to include in the request.

    Returns:
        dict: The response data from the API.

    """
    # Construct the query string from the parameters
    query_string = '&' + '&'.join((f"{key}={value}" if value!="" else f"{key}") for key, value in params.items()) if params else ""
    full_url = f"{api_url}{endpoint}?api_key={api_key}{query_string}"
    # Send the request
    res = requests.get(full_url)
    res = res.json()["response"] if not("_view" in params.keys()) else res.json()
    
    return res

# Function to format the data
def format_data(res):
    """
    Format the data received from the API.

    Args:
        res (list): The raw data received from the API.

    Returns:
        list: The formatted data.

    """
    res = [
        {"position": {
                            "lat": x.pop("lat", None),
                            "lon": x.pop("lng", None),
                        }
        , **x}
        for x in res
    ]
    return res

