import json
import csv

with open('tone.json') as json_file:
    data = json.load(json_file)

columns = list(data[0].keys())

with open('tone.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(columns)

    for item in data:
        row = list(item.values())
        writer.writerow(row)