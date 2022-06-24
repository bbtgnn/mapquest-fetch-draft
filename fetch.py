### IMPORTS

import csv
import urllib.request
import urllib.parse
import time



### VARIABLES

key = '<MAPQUEST_KEY>'

csvpath = './data.csv'

city = 'San Giacomo Filippo'
postalcode = '23020'
state = 'Italia'



### DEFINITIONS

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))



### INSTRUCTIONS

## -- Getting data from csv -- ##

data = []

with open(csvpath, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        data.append(row[0])


## -- Creating queries -- ##

queries = []

# Splitting data in chunks
chunks = [x for x in chunker(data, 90)]

# Iterating over chunks
for c in chunks:
    # Building query
    query = ''

    # Adding &location= for each address
    for address in c:
        fullAddress = f"{city}, {postalcode}, {address}, {state}"
        fullAddress = urllib.parse.quote(fullAddress)
        query += f'&location={fullAddress}'

    queries.append(query)


## -- Making requests -- ##

for q, query in enumerate(queries):

    # Building request url
    url = f'http://www.mapquestapi.com/geocoding/v1/batch?key={key}{query}'

    # Making request
    with urllib.request.urlopen(url) as response:
        # Decoding response
        res = response.read().decode('utf-8')
        # Writing to json
        with open(f'fetch-{q}.json', 'w') as f:
            f.write(res)

    # Waiting a bit before next request
    time.sleep(5)
