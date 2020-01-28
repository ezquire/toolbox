import os
import csv
import glob
import argparse
import pandas as pd

def combine():
    file_path_pattern = '/Users/tylergearing/Downloads/*.xlsx'
    workbooks = glob.glob(file_path_pattern)
    all_data = pd.DataFrame()
    for wb in workbooks:
        df = pd.read_excel(wb)
        df.sort_index(inplace=True, axis=1)
        all_data = all_data.append(df, ignore_index=True, sort=True)
    export_csv = all_data.to_csv(r'combined.csv', index=None, header=True)

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.parse_args()

def main():
    init_parser()

if __name__ == '__main__':
    main()
