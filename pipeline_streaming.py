from apache_beam.options.pipeline_options import PipelineOptions
from google.cloud import pubsub_v1
from google.cloud import bigquery
import apache_beam as beam
import logging
import argparse
import sys
import re


PROJECT= "lucid-destiny-262216"
TOPIC = "projects/lucid-destiny-262216/topics/car-traffic"
schema = 'region:STRING, region_id:INTEGER, location_description:STRING, current_speed:FLOAT, timestamp:DATETIME, west:STRING, east:STRING, south:STRING, north:STRING'
#TOPIC = "projects/user-logs-237110/topics/userlogs"


def regex_clean(data):

	PATTERNS =  [r'(^\S+\.[\S+\.]+\S+)\s',r'(?<=\[).+?(?=\])',
		   r'\"(\S+)\s(\S+)\s*(\S*)\"',r'\s(\d+)\s',r"(?<=\[).\d+(?=\])",
		   r'\"[A-Z][a-z]+', r'\"(http|https)://[a-z]+.[a-z]+.[a-z]+']
	result = []
	for match in PATTERNS:
		try:
			reg_match = re.search(match, data).group()
			if reg_match:
				result.append(reg_match)
			else:
				result.append(" ")
		except:
			print("There was an error with the regex search")
	result = [x.strip() for x in result]
	result = [x.replace('"', "") for x in result]
	res = ','.join(result)
	return res


class Split(beam.DoFn):

	def process(self, element):
		from datetime import datetime
		element = element.split(",")
		print(element)
		d = datetime.strptime(element[1], "%d/%b/%Y:%H:%M:%S")
		date_string = d.strftime("%Y-%m-%d %H:%M:%S")
		
		return [{ 
			'region': element[0],
			'region_id': int(element[1]),
			'west': element[2],
			'east': element[3],
			'north': element[4],
			'south': element[5],
			'location_description': element[6],
			'current_speed': float(element[7]),
			'timestamp': date_string
		}]

def main(argv=None):

	parser = argparse.ArgumentParser()
	parser.add_argument("--input_topic")
	parser.add_argument("--output")
	known_args = parser.parse_known_args(argv)


	p = beam.Pipeline(options=PipelineOptions())
	print("OK")
	(p
		| "ReadData" >> beam.io.ReadFromPubSub(topic=TOPIC).with_output_types(bytes)
		| "Decode" >> beam.Map(lambda x: x.decode('utf-8'))
		| "Print Data" >> beam.Map(print)
	  #| "Clean Data" >> beam.Map(regex_clean)
	    | 'ParseCSV' >> beam.ParDo(Split())
	    | 'WriteToBigQuery' >> beam.io.WriteToBigQuery('{0}:car_traffic_dataset.car_traffic_better'.format(PROJECT), schema=schema,
	    	write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
	)
	result = p.run()
	result.wait_until_finish()

if __name__ == '__main__':
  logger = logging.getLogger().setLevel(logging.INFO)
  main()