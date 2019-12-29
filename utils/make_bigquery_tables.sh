#!/bin/bash

bq mk --table $PROJECT:$DATABASE_NAME.$MAIN_TABLE_NAME ./data/schema/car_traffic_schema.json

bq mk --table $PROJECT:$DATABASE_NAME.$HISTO_TABLE_NAME ./data/schema/car_traffic_historique_schema.json

bq mk --table $PROJECT:$DATABASE_NAME.$CORRESP_TABLE_NAME ./data/schema/corresp_schema.json

bq mk --table $PROJECT:$DATABASE_NAME.$TMP_TABLE_NAME ./data/schema/car_traffic_schema.json

