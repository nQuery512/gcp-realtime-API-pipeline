import json

with open("./data/tmp_data.json", 'r+') as json_file:
    text = json_file.read()
    json_data = json.loads(text)
    #print(json_data)
    for e in json_data:
        e['p1'] = str(e['_north'] + ', ' + e['_west'])
        e['p2'] = str(e['_south'] + ', ' + e['_east'])
        del e['_north'], e['_south'], e['_west'], e['_east']
with open("./data/tmp_data_final.json", 'w') as json_file_final:
    print(json_data)
    json.dump(json_data, json_file_final)

