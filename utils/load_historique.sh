wget https://data.cityofchicago.org/api/views/emtn-qqdi/rows.csv?accessType=DOWNLOAD&bom=true&format=true&delimiter=%3B -O ./data/chicago_traffic_dataset_2013_2018.csv &&
bq load --source_format=CSV --skip_leading_rows=1 burnished-range-263415:car_traffic_dataset.car_traffic_historique ./data/chicago_traffic_dataset_2013_2018.csv myschema.json &&
echo "Construction de la table de correspondance..." &&
bq query < make_corresp_table.sql &&
#sleep 60 
echo "Enrichissement de l'historique..." &&
bq query < enrich_historique.sql &&
#sleep 60
echo "Fusion des tables..." &&
bq query < join_with_realtime.sql
#sleep 60
