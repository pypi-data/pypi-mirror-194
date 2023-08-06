import sys, os, getopt
import pandas as pd

def fitscores(input_loc, output_loc, rawfile):

    # Make sure all columns are loaded
    pd.set_option("display.max_colwidth", None)

    # Load cdata and rawdata from input_loc and rawfile
    cdata = pd.read_csv(input_loc)
    raw = pd.read_csv(rawfile)

    # Subset cdata for rows containing coordinates
    datasubset = cdata.loc[cdata["Score"] != "Skip"].reset_index().iloc[:, 1:]

    # Reset USI Unique_Spot_ID column
    for row in range(0, len(datasubset)):
        datasubset.loc[row, "Unique_Spot_ID"] = 'S' + str(row+1)

    # Fill Score and Replicate columns from rawdata
    datasubset["Score"] = raw["Score"]
    datasubset["Replicate"] = raw["Replicate"]

    # Save scored dataframe to output location
    datasubset.to_csv(output_loc, index=False)
