import request_api
import logging
from google.cloud import pubsub_v1
import time
import os
import json

PROJECT_ID = os.environ['PROJECT']
TOPIC = os.environ['TOPIC_NAME']
EXTERNAL_API_URL = os.environ['EXTERNAL_API_URL']
EXTERNAL_API_KEY = os.environ['EXTERNAL_API_KEY']

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC)

def publish(publisher, topic_path, data_lines):
	print(data_lines)
	return publisher.publish(topic_path, data = data_lines.encode('utf-8'))

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

        message_future = publish(publisher, topic_path, data)
        message_future.add_done_callback(callback)

        sleep_time = 1200
        time.sleep(sleep_time)
