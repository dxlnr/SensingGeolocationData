"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

__author__ = "gregorjahner"

# Import points from a text file
import rhinoscriptsyntax as rs
import csv
import ghpythonlib.treehelpers as th
#import pandas as pd

def calTotalNumberOfSpots():
    #df = pd.read_csv("top_spots.csv", usecols = ['0'])
    #return df['0'].sum()
    pass


def CSVlist():
    #prompt the user for a file to import
    filter = "CSV file (*.csv)|*.csv|*.txt|All Files (*.*)|*.*||"
    filename = rs.OpenFileName("top_spots", filter)
    if not filename: return

    tmplist = list()
    with open(filename) as csvfile:
    #with open('top_spots.csv') as csvfile:
        reader = csv.reader(csvfile)
        #reader = csv.reader(csvfile, delimiter=',')
        header_idx = True
        for row in reader:
            if header_idx == True:
                header_idx = False
                #print(row)
                continue

            lat = float(row[0])
            long = float(row[1])
            alt = float(row[2])
            print(lat, long, alt)

            rs.AddPoint(lat, long, alt)
            tmplist.append([lat, long, alt])
    print(tmplist)
    b = th.list_to_tree(tmplist)
    return b

"""
if( __name__ == "__main__" ):
    CSVlist()
    #calTotalNumberOfSpots()

"""
b = CSVlist()

