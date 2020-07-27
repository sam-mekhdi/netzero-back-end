import csv
import json

output = {'Transactions': []}

with open('mockdata.csv') as csv_file:
    with open('./mockdata.json', 'w') as jsonfile:
        for Transactions in csv.DictReader(csv_file):
            output['Transactions'].append({
                    'studentNumber': Transactions['studentNumber'],
                    'transactionID': Transactions['transactionID'],
                    'itemName': Transactions['itemName'],
                    'location': Transactions['location'],
                    'quantity': Transactions['quantity'],
                    'date': Transactions['date'],
                    'time': Transactions['time']
            })           
           
        json.dump(output, jsonfile, sort_keys=True, indent=4)
        jsonfile.write('\n')