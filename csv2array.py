import csv

results = []
with open('EarnUp Custody Nodes.csv') as csvfile, open('EarnUp Custody Nodes.txt', 'w') as outfile:
    reader = csv.reader(csvfile)
    for row in reader:
        results.append(row[0])
    outfile.write(str(results))