import time
import json
import os



def testing_module(producer, filename='dummy_data.json'):
    file_path = f'utils/{filename}'
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"JSON file '{filename}' does not exist. Please create it using: python kafka_stream.py export --filename {filename}")
        return

    with open(file_path, 'r') as file:
        data = json.load(file)

    print(f"Starting to send {len(data)} messages...")
    for i, obj in enumerate(data, 1):
        producer.send('flight', obj)
        print(f"Sent message {i}/{len(data)}")
        time.sleep(0.05)
    producer.flush()
    print("All messages sent successfully!")


