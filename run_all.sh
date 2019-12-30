#!/bin/bash

#echo "\nChargement de l'environement"
#source ./utils/set_env_encrypted.sh
rm ./data/tmp_data.json ./data/tmp_data_final.json
echo "\nCréation des tables..."
sh ./utils/make_bigquery_tables.sh

echo "\nObtention et modifications des données historique..."
## Test d'existence du fichier
[ -f ./data/chicago_car_traffic_2013_2018.csv ] && echo "\nINFO: Historique déjà présent" || wget -O ./data/chicago_car_traffic_2013_2018.csv "https://data.cityofchicago.org/api/views/emtn-qqdi/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B" && sed -i "1 s/ //g; s/REGION_ID/_REGION_ID/g; s/BUSCOUNT/BUS_COUNT/g; s/NUMBEROFREADS/NR/g;" ./data/chicago_car_traffic_2013_2018.csv

echo "\nObtention des données temporaire..."
## Test d'existence du fichier
curl $EXTERNAL_API_URL/?%24%24app_token=$EXTERNAL_API_KEY > ./data/tmp_data.json
python3 add_location_good_format.py
cat ./data/tmp_data_final.json | jq -c ".[]" > ./data/tmp_data_finall.json
mv ./data/tmp_data_finall.json ./data/tmp_data_final.json

echo "\nAlimentation de la table temporaire..."
bq load --source_format=NEWLINE_DELIMITED_JSON $PROJECT:$DATABASE_NAME.$TMP_TABLE_NAME ./data/tmp_data_final.json ./data/schema/car_traffic_schema.json

echo "\nAlimentation de la table historique"
bq load --source_format=CSV --skip_leading_rows=1 --field_delimiter=';' $PROJECT:$DATABASE_NAME.$HISTO_TABLE_NAME ./data/chicago_car_traffic_2013_2018.csv ./data/schema/car_traffic_historique_schema.json
exit
echo "\nAlimentation de la table de correspondance"
bq query < ./bigquery/make_corresp_table.sql

echo "\nEnrichissement de l'historique"
bq query < ./bigquery/enrich_historique.sql

echo "\nFusion des données historique avec les données temps réels"
bq query < ./bigquery/join_with_realtime.sql
