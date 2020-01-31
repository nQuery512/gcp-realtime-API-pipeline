#standardSQL
UPDATE `car_traffic_dataset.car_traffic_historique` histo 
SET histo._description = corresp._description, histo.region = corresp.region, histo.p1 = corresp.p1, histo.p2 = corresp.p2
FROM `car_traffic_dataset.table_correspondance` corresp
WHERE histo._region_id = corresp._region_id
