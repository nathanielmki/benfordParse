from email import header
from operator import index
import os
import csv
import sys
import argparse

from collections import Counter
from math import log10
from xml.etree.ElementInclude import include

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import benford as bf

def benfordParse(infile = "", outfile=None, analysis_column="", index_column="", header_status=""):

    # create dataframe of uploaded file, 
    # engine is specified to allow python to determine delimiter
    df = pd.read_csv(infile, sep=None, engine='python')

    # create dataframe based upon user defined analysis column
    analysis_data = df[analysis_column]

    #print(analysis_data)

    #analysis_data.describe()
    #analysis_data.info()

    ##################################### using benford lib #############################

    # perform Benford test on selected data
    f1d = bf.first_digits(analysis_data, digs=1, save_plot=outfile)
    print(f1d)
    
    # if outfile name is given, saves output to disk 
    if outfile !=None:
        f1d.to_csv(outfile, encoding='utf-8', index=False)
    else:
        print(f1d)

def main():
    # Definitions for available arguments
    parser = argparse.ArgumentParser(
        description='Load input file for Benford parsing')
    
    parser.add_argument("-i", "--infile", required=True, dest="infile",
                        help="Input data file to parse through")

    parser.add_argument("-o", "--outfile", dest="outfile",
                        help="Optional output filename. If not given, results will be printed to terminal")
    
    parser.add_argument("-ac", "--analysis_col", required=True, dest="analysis_column",
                        help="Column name to process through parser")

    parser.add_argument("-hs", "--header_status", dest="header_status",
                        help="If header exists on file, leave blank. If there is no header on datafile, set to None")
    
    benfordParse(**vars(parser.parse_args()))
if __name__ == '__main__':
    main()