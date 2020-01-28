import os
import csv
import glob
import argparse
import pandas as pd

def combine(path, outfile):
    file_path = path
    file_path_pattern = path + '*.xlsx'
    workbooks = glob.glob(file_path_pattern)
    all_data = pd.DataFrame()
    for wb in workbooks:
        df = pd.read_excel(wb)
        df.sort_index(inplace=True, axis=1)
        all_data = all_data.append(df, ignore_index=True, sort=True)
    export_csv = all_data.to_csv(outfile, index=None, header=True)

def init_parser():
    parser = argparse.ArgumentParser(description='Generate an combined csv file from .xlsx extensions')
    parser.add_argument('path', help="Path to folder containing .xlsx files to combine")
    parser.add_argument('-o', '--output-file', type=str, default=None, help="Path to csv file to output")
    args = parser.parse_args()
    return args


def main():
    args = init_parser()
    outfile = args.output_file
    if outfile is None:
        combine(args.path, r'combined.csv')
    else:
        combine(args.path, outfile)
    

if __name__ == '__main__':
    main()