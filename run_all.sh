#!/bin/bash

#echo "\nChargement de l'environement"
#source ./utils/set_env_encrypted.sh

echo "\nCréation des tables..."
sh ./utils/make_bigquery_tables.sh

echo "\nObtention des données historique..."
## Test d'existence du fichier
[ -f ./data/chicago_car_traffic_2013_2018.csv ] && echo "\nINFO: Historique déjà présent" || wget -O ./data/chicago_car_traffic_2013_2018.csv "https://data.cityofchicago.org/api/views/emtn-qqdi/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B"

echo "\nObtention des données temporaire..."
## Test d'existence du fichier
[ -f ./data/tmp_data.json ] && echo "\nDonnées temporaires déjà présentes" || curl $EXTERNAL_API_URL/?%24%24app_token=$EXTERNAL_API_KEY > ./data/tmp_data.json

echo "\nChargement de la table temporaire..."
bq load --source-format=JSON $PROJECT:$DATABASE_NAME.$TMP_TABLE_NAME ./data/tmp_data.json ./data/schema/car_traffic_schema.json

echo "\nAlimentation de la table historique"
bq load --source_format=CSV --skip_leading_rows=1 $PROJECT:$DATABASE_NAME.$HISTO_TABLE_NAME ./data/chicago_car_traffic_2013_2018.csv car_traffic_historique_schema.json

echo "\nAlimentation de la table de correspondance"
bq query < ./bigquery/make_corresp_table.sql

echo "\nEnrichissement de l'historique"
bq query < ./bigquery/enrich_historique.sql

echo "\nFusion des données historique avec les données temps réels"
bq query < ./bigquery/join_with_realtime.sql
