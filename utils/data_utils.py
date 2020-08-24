import os
import numpy as np
import pandas as pd
import csv

from pathlib import Path

file = Path(__file__)
ROOT_PATH = file.parent.parent
DATA_PATH = ROOT_PATH.joinpath("data")

class DataLoader():

    def __init__(self):
        pass


    def read_files(self):
        '''
        Reading in the .csv datafiles and concatenate them together in one dataframe.
        :returns concatenated datafiles (.csv) as a pandas dataframe.
        '''
        counter = 0
        for file in os.listdir(DATA_PATH):
            filename = os.fsdecode(file)
            if filename.endswith(".csv"):
                counter += 1
                df = pd.read_csv(os.path.join(DATA_PATH, filename), delimiter=',', encoding="utf-8-sig")
                df.rename(columns=lambda x: x.strip(), inplace=True)

                df = df.drop_duplicates(subset=['Timestamp'])

                if counter == 1:
                    df_complete = df
                    continue

                frames = [df_complete, df]
                df_complete = pd.concat(frames)

            else:
                print("Error encountered while parsing file: ", filename)

        print('Dataframe shape: ', df_complete.shape, '    ', '(from read_files)')
        #print(df_complete.head(20))

        return (df_complete)


    def convert_to_np(self, dataframe, dimension=2):
        # Convert pandas dataframe to numpy array
        if dimension == 2:
            array = dataframe[['Latitude','Longitude']].to_numpy()
        elif dimension == 3:
            array = dataframe[['Latitude','Longitude', 'Altitude']].to_numpy()
        else:
            print("Error occured - dimensionality is illegal: ", dimension)

        #np.swapaxes(array, 0, 1)

        return (array)


    def drop_nth_row(self, dataframe, nth_row=2):
        '''
        :params dataframe: pandas dataframe.
        :params nth_row: Selects every nth row starting from 0.
        :returns pandas dataframe with reduced number of rows.
        '''
        df_reduced = dataframe[dataframe.index % nth_row == 0]
        return (df_reduced)


    def find_popular_spots(self, dataframe, rank, dimension=3):
        '''
        Built to find duplicates that show us the top ranked spots in the dataframe.
        :params dataframe: pandas dataframe.
        :params rank: Integer that defines the number of spots.
        :returns pandas dataframe with top ranked datapoints.
        '''
        if dimension == 2:
            pivt = dataframe.pivot_table(index=['Latitude', 'Longitude'], aggfunc='size').sort_values(ascending=False)
        elif dimension == 3:
            pivt = dataframe.pivot_table(index=['Latitude', 'Longitude', 'Altitude'], aggfunc='size').sort_values(ascending=False)
        else:
            print("Error occured - dimensionality is illegal: ", dimension)

        tops = pivt.iloc[:rank]
        return (tops.reset_index())


    def drop_duplicates(self, dataframe, dist=0.0001):
        # Dropping the spatioal coordinates that are saved in the dataset more than one time.
        return dataframe.drop_duplicates(subset=['Latitude', 'Longitude', 'Altitude'])

    def sort_around_area(self, df):
        '''
        Function computes distances from topspot and drops the ones that too far.
        Be cautious! (Runtime)
        :params df: pandas dataframe.
        '''
        top_spot = self.find_popular_spots(df, rank=1)
        df_result = self.drop_duplicates(df)

        df_result = df_result.loc[:,~df_result.columns.duplicated()]
        df_result['Distance'] = np.nan
        df_result.reset_index(inplace=True)

        for i in range(len(df_result.index)):
            dist = np.sqrt(np.power((top_spot.iloc[0]['Latitude'] - df.iloc[i]['Latitude']), 2) + \
            np.power((top_spot.iloc[0]['Longitude'] - df.iloc[i]['Longitude']), 2))

            df_result.loc[i, 'Distance'] = dist
            if dist >= 0.0001:
                df_result.drop(i, inplace=True)

        return (df_result)


    def find_points_jslm(self, df):
        '''
        Function filters dataframe in the area of Jerusalem.
        :params df: pandas dataframe.
        '''

        long_min = 35.174
        long_max = 35.274
        lat_min = 31.72
        lat_max = 31.822

        df.reset_index(inplace=True)

        indexNames = df[(df['Longitude'] >= long_max) | (df['Longitude'] <= long_min) | \
                        (df['Latitude'] >= lat_max) | (df['Latitude'] <= lat_min)].index
        df.drop(indexNames , inplace=True)

        return (df)
