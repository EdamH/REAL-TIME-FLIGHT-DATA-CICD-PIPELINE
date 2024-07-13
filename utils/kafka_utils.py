from kafka import KafkaProducer
import json
import time
import logging
from utils.api_utils import get_data, format_data



# Create a Bootstrap Server
bootstrap_servers = 'localhost:9093'
# Create a Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# API URL and Key
api_endpoint = 'flights'

# Kafka Topic
flight_topic = "flight" 
_fields = "hex,\
        reg_number,\
        flag,\
        lat,\
        lng,\
        alt,\
        dir,\
        speed,\
        v_speed,\
        flight_number, \
        flight_icao,\
        flight_iata,\
        dep_icao,\
        dep_iata,\
        arr_icao,\
        arr_iata,\
        airline_icao,\
        airline_iata,\
        aircraft_icao,\
        status" 


def stream_data(endpoint, fields, interval = 60):
    """
    Stream data from the API to Kafka.

    Args:
        endpoint (str): The API endpoint to retrieve data from.
        fields (str): The fields to include in the API response.

    Returns:
        None

    """
    curr_time = time.time()
    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        try:
            res = get_data(endpoint, 
               _fields=fields
            )
            res = format_data(res)
            print(res[0])
            print(len(res))
            # Send each object in the list to Kafka
            for obj in res:
                producer.send('flight', obj)
                time.sleep(0.05)
            producer.flush()
            
            time.sleep(interval) # Sleep for 60 seconds for request management
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue



