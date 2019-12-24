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
schema = 'region:STRING, region_id:INTEGER, _description:STRING, current_speed:FLOAT, _last_updt:DATETIME, _west:FLOAT, _east:FLOAT, _south:FLOAT, _north:FLOAT'
TOPIC_NAME = os.environ['TOPIC_NAME']
DATABASE_NAME = os.environ['DATABASE_NAME']
TABLE_NAME = os.environ['TABLE_NAME']
TOPIC = "projects/"+PROJECT+"/topics/"+TOPIC_NAME
print(TOPIC)

DB_URI = PROJECT+':'+DATABASE_NAME+'.'+TABLE_NAME
print("\n\n\n"+DB_URI+"\n\n\n")
class ParseData(beam.DoFn):

    def process(self, element):
        res = []
        #  print(element)
        json_data = json.loads(element)
        json_data = json_data['messages']
        for elem in json_data:
#            print(elem['data'])
            res.append(elem['data'])
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
