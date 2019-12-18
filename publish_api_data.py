import request_api
import logging
from google.cloud import pubsub_v1
import random
import time
import os

PROJECT_ID= "lucid-destiny-262216"
TOPIC = "car-traffic"
EXTERNAL_API_URL = os.environ['EXTERNAL_API_URL']
EXTERNAL_API_KEY = os.environ['EXTERNAL_API_KEY']

#print(os.environ['EXTERNAL_API_URL'])

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

def publish(publisher, topic, message):
    data = message.encode('utf-8')
    return publisher.publish(topic_path, data = data)

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
    else:
        print(message_future.result())

if __name__ == '__main__':

    while True:
        data = request_api.retrieve_data_from_api(EXTERNAL_API_URL, EXTERNAL_API_KEY)
        #print(type(data))
        print(data)
        message_future = publish(publisher, topic_path, data)
        message_future.add_done_callback(callback)

        sleep_time = random.choice(range(1, 3, 1))
        time.sleep(sleep_time)
