from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import pubsub_v1
from google.cloud import bigquery
import apache_beam as beam
import logging
import argparse
import sys
import re
import os
import json

PROJECT = os.environ['PROJECT']
schema = 'region:STRING, _region_id:INTEGER, _description:STRING, current_speed:FLOAT, _last_updt:DATETIME, _west:FLOAT, _east:FLOAT, _south:FLOAT, _north:FLOAT'
TOPIC_NAME = os.environ['TOPIC_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']
MAIN_TABLE_NAME = os.environ['MAIN_TABLE_NAME']
TOPIC = "projects/"+PROJECT+"/topics/"+TOPIC_NAME
print("Subscribing to "+TOPIC)

DB_URI = PROJECT+':'+DATABASE_NAME+'.'+TABLE_NAME
print("\n"+DB_URI+"\n")
class ParseData(beam.DoFn):

    def process(self, element):

        res = json.loads(element)
	for e in res:
                e['p1'] = str(e['_north'] + ', ' + e['_west'])
                e['p2'] = str(e['_south'] + ', ' + e['_east'])
                del e['_north'], e['_south'], e['_west'], e['_east']

        print(type(res))
        print(res)
        return res

def main(argv=None):

   parser = argparse.ArgumentParser()
   parser.add_argument("--input_topic")
   parser.add_argument("--output")
   known_args = parser.parse_known_args(argv)


   p = beam.Pipeline(options=PipelineOptions())

   (p
      | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
      | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
      | "ParseJSON" >> beam.ParDo(ParseData())
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(PROJECT+':'+DATABASE_NAME+'.'+TABLE_NAME, schema=schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
   )
   result = p.run()
   result.wait_until_finish()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()
