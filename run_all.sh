#!/bin/bash

echo "Création des tables..."
sh make_bigquery_tables.sh

echo "Obtention des données historique..."
[ -f ./data/chicago_car_traffic_2013_2018.csv ] && echo "Historique déjà présent" || wget -O ./data/chicago_car_traffic_2013_2018.csv "https://data.cityofchicago.org/api/views/emtn-qqdi/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B"

echo "Obtention des données temporaire..."
curl $EXTERNAL_API_URL/?%24%24app_token=$EXTERNAL_API_KEY > ./data/tmp_data.json

