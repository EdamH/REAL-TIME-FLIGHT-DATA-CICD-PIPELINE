import argparse
from utils.testing_utils import testing_module
from utils.kafka_utils import stream_data, _fields, api_endpoint, producer
from utils.api_utils import export_data_to_json

if __name__ == "__main__":
    """
    Main script for handling different modes of operation.

    Modes:
    - stream: Streams data using Kafka.
    - export: Exports data from the airlab API endpoint to a JSON file for testing purposes.
    - test: Tests a module with data from said JSON file.

    Command-line Arguments:
    - mode: Choose the mode to run the script: stream, test, or export.
    - --filename (optional): Specify the filename for export or testing modes (defaults to 'dummy_data.json').

    Example Usage:
    - Stream data: python main_script.py stream
    - Export data to a custom filename: python main_script.py export --filename custom_data.json
    - Test module with a custom filename: python main_script.py test --filename custom_data.json
    """


    parser = argparse.ArgumentParser(description='Choose the mode to run the script.')
    parser.add_argument('mode', choices=['stream', 'test', 'export'], help='Mode to run the script: stream, test, or export')
    parser.add_argument('--f', type=str, default='dummy_data.json', help='Specify the JSON filename for export or testing modes (optional)')

    args = parser.parse_args()

    if args.mode == 'stream':
        stream_data(api_endpoint, _fields, 2)
    elif args.mode == 'export':
        export_data_to_json(api_endpoint, _fields, filename=args.f)
    elif args.mode == 'test':
        testing_module(producer, filename=args.f)
