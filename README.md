# Realtime Google Cloud Pipeline with and without Apache Beam
- [X] Acquire and ingest real-time events from external API using google Pub/Sub
- [X] Pipeline using gcloud library
- [X] Pipeline using Apache Beam
- [x] Acquire and ingest static files 
- [x] Store raw data in BigQuery
- [x] Create new BigQuery table using transformation (handle real-time ?)
- [ ] Data visualization using google cloud tools (datastudio?) and/or WebApp (AppEngine)

![Realtime pipeline schema](https://cloud.google.com/dataflow/images/diagram-dataflow.png) (This image is a property of Google)

## Ingestion pipeline description
Cloud Pub/Sub -> Apache Beam+Cloud DataFlow -> BigQuery

Using 1 Cloud Compute Engine instance, but can run in properly configured local environment

## How to run

First you MUST modify set_env_encrypted.sh to match your environment

### Prerequisite
```shell
sudo sh install-deps.sh
source ./set_env_encrypted.sh
 
```

### Publisher
```shell
python3 publish_api_data.py 
```

### Pipeline without Apache Beam

#### Pipeline Sub -> BigQuery in local mode (without DataFlow)
```shell 
python3 pipeline_streaming.py --streaming
```

** OR **

#### Pipeline Sub -> BigQuery with DataFlow
```shell
python3 pipeline_streaming.py --project $PROJECT --temp_location $BUCKET/tmp --staging_location $BUCKET/staging --streaming
```

### Pipeline using Apache Beam
#### Pipeline Sub -> BigQuery in local mode (without DataFlow)
```shell
python3 pipeline_streaming_beam.py --streaming
```

#### Pipeline Sub -> BigQuery with DataFlow
```shell
python3 pipeline_streaming_beam.py --project $PROJECT --temp_location $BUCKET/tmp --staging_location $BUCKET/staging --streaming
``` 
