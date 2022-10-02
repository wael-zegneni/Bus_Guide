from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time


# READ COORDINATES FROM GEOJSON

input_file = open('./venv/data/bus2.json')  # opening the json file
json_array = json.load(input_file)  # json conversion
coordinates = json_array['features'][0]['geometry']['coordinates']  # to have the list of all the coordinates


# GENERATE UUID
def generate_uuid():
    return uuid.uuid4()


client = KafkaClient(hosts="localhost:9092")  # where kafka is running
topic = client.topics['geodata_final123']  # topic
producer = topic.get_sync_producer()  # producer

# CONSTRUCT MESSAGE AND SEND IT TO KAFKA
data = {}
data['busline'] = '00002'

def generate_checkpoint(coordinates):  # for each coordinate we generate new data
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())  # gives you the current time
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)  # create message in json format
        print(message)
        producer.produce(message.encode('ascii'))  # sending data to kafka
        time.sleep(1)

        # if the bus tousel l ekher coordiate, taawed mel issat ;)
        if i == len(coordinates) - 1:  # boucle infinie
            i = 0
        else:
            i += 1


generate_checkpoint(coordinates)
