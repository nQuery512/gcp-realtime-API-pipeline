from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import pubsub_v1 as pubsub
from google.cloud import bigquery
import apache_beam as beam
import logging
import argparse
import sys
import re
import os
import base64
import json

PROJECT_NAME = os.environ["PROJECT"]
TOPIC_NAME = os.environ['TOPIC_NAME']
SUBSCRIBE_NAME = os.environ["SUBSCRIBE_NAME"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
TABLE_NAME = os.environ["TABLE_NAME"]

def write_to_bigquery(dataset_id, table_id, messages):
	client = bigquery.Client()
	dataset_ref = client.dataset(dataset_id)
	table_ref = dataset_ref.table(table_id)
	table = client.get_table(table_ref)

	errors = client.insert_rows(table, messages)
	if not errors:
		print('Loaded {} row(s) into {}:{}'.format(len(messages), dataset_id, table_id))
	else:
		print('Errors:')
		for error in errors:
			print(error)

def collect_data(data):
	res = json.loads(data.decode('utf-8'))
	print(res)
	write_to_bigquery(DATABASE_NAME, TABLE_NAME, res)

def receive_message(project, subscription_name):
    subscriber = pubsub.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        collect_data(message.data)
        message.ack()

    future = subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))

    try:
        future.result(timeout=30)
    except Exception as e:
        print(
            'Listening for messages on {} threw an Exception: {}'.format(
                subscription_name, e))
        raise

    while True:
        time.sleep(60)

if __name__ == '__main__':
	logger = logging.getLogger().setLevel(logging.INFO)
	receive_message(PROJECT_NAME, SUBSCRIBE_NAME)
