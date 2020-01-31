#standardSQL
INSERT INTO `car_traffic_dataset.table_correspondance` (_region_id, _description, region, p1, p2)
SELECT _region_id, _description, region, p1, p2
FROM `car_traffic_dataset.car_traffic_temp`
GROUP BY _region_id, _description, region, p1, p2
