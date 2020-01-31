#standardSQL
INSERT INTO `car_traffic_dataset.car_traffic`
SELECT SPEED AS current_speed, _REGION_ID AS _region_id, region, _description, p1, p2, TIME AS _last_updt
FROM `car_traffic_dataset.car_traffic_historique` as histo
