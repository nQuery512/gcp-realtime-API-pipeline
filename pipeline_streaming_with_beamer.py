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
schema = 'region:STRING, region_id:INTEGER, _description:STRING, current_speed:FLOAT, _last_updt:DATETIME, _west:STRING, _east:STRING, _south:STRING, _north:STRING'
TOPIC_NAME = os.environ['TOPIC_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
TOPIC = "projects/"+PROJECT+"/topics/"+TOPIC_NAME
print(TOPIC)

class PrintData(beam.DoFn):
    def process(self, element):
        print(element)
        return element

def main(argv=None):

   parser = argparse.ArgumentParser()
   parser.add_argument("--input_topic")
   parser.add_argument("--output")
   known_args = parser.parse_known_args(argv)


   p = beam.Pipeline(options=PipelineOptions())

   (p
      | 'ReadData' >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
      | "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
      | "ParseJSON" >> beam.Map(json.loads)
#      | "Print Data" >> beam.Map(PrintData)
     # | "Clean Data" >> beam.Map(json.dumps)
     # | 'ParseCSV' >> beam.ParDo(Split())
      | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(PROJECT+':'+DATABASE_NAME+'.'+TABLE_NAME, schema=schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
   )
   result = p.run()
   result.wait_until_finish()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()
