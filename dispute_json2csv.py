import json
import csv
import glob
import os
import datetime as dt

cwd = os.getcwd() + "/"
filepath = cwd + "*.json"
files = glob.glob(filepath)

with open(cwd + 'Dispute Report ' + str(dt.datetime.now().date()) + '.csv', 'a') as output:
    writeHeader = True
    for f in files:
        with open(f) as json_file:
            # read json
            data = json.load(json_file)
            # create csvwriter
            csvwriter = csv.writer(output)
            for report in data["dispute_report"]:
                if writeHeader:
                    csvwriter.writerow(report.keys())
                    writeHeader = False
                csvwriter.writerow(report.values())