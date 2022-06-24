import json
import glob
import csv


# Getting all the json files
files = []
for file in glob.glob('./*.json'):
    files.append(file)

# Sorting
files.sort()

# Getting all the json
jsons: list[dict] = []
for path in files:
    with open(path, 'r') as file:
        data = json.load(file)
        jsons.append(data)

# Getting all the results
results: list[dict] = []
for json in jsons:
    results.extend(json['results'])

# Making a dictionary where keys are data.csv entries
resultsDict: dict = {}
for res in results:
    key = res['providedLocation']['location'].split(',')[2].strip()
    resultsDict[key] = res

# Reading keys from the csv lines
keys = []
with open('./data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        keys.append(row[0])

# Writing the table
table = []
for key in keys:
    # Creating empty row
    row = []
    # Adding the key
    row.append(key)
    # Getting the matching result
    res = resultsDict[key]
    # Saving the location
    for loc in res['locations']:
        row.append('@')
        row.append(loc['street'])
        row.append(loc['latLng']['lat'])
        row.append(loc['latLng']['lng'])
    # Adding to table
    table.append(row)

# Writing csv
with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    for row in table:
        writer.writerow(row)