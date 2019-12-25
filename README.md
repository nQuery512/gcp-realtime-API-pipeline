# Realtime Google Cloud Pipeline with and without Apache Beam
- [X] Acquire and ingest real-time events from external API using google Pub/Sub
- [X] Pipeline using gcloud library
- [X] Pipeline using Apache Beam
- [ ] Acquire and ingest static files 
- [x] Store raw data in BigQuery
- [x] Create new BigQuery table using transformation (handle real-time ?)
- [ ] Data visualization using google cloud tools and/or WebApp (AppEngine)

![Realtime pipeline schema](https://cloud.google.com/dataflow/images/diagram-dataflow.png) (This image is a property of Google)

## Ingestion pipeline description
Cloud Pub/Sub -> Apache Beam+Cloud DataFlow -> BigQuery

Using 1 Cloud Compute Engine instance, but can run in properly configured local environment

