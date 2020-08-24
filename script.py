import os
import sys
print(sys.version)
import numpy as np
import pandas as pd
import geopandas as gpd


# Print the whole numpy array
#np.set_printoptions(threshold=sys.maxsize)

from utils.data_utils import *
from utils.vis_utils import *
from utils.model import *


if __name__ == "__main__":
    # Instantiate the dataloader object.
    dl = DataLoader()

    # prepare the dataframe for further actions.
    org_data = dl.read_files()
    w_o_dup_data = dl.drop_duplicates(org_data)

    # Visualize all the pts.
    x = dl.convert_to_np(w_o_dup_data)
    visualize_np_array(x)

    df_top_spots = dl.find_popular_spots(org_data, rank=100)
    df_top_spots.to_csv("top_spots_100.csv", encoding='utf-8', index=False)


    jlm_df = dl.find_points_jslm(org_data)
    jlm_np = dl.convert_to_np(jlm_df)
    print("shape of dataframe Jerusalem: ", jlm_np.shape)
    visualize_np_array(jlm_np)

    df_top_spots_jlm = dl.find_popular_spots(jlm_df, rank=100)
    df_top_spots_jlm.to_csv("top_spots_100_JSLM.csv", encoding='utf-8', index=False)

    vis_map_png_data(w_o_dup_data, 'map.png')

    """
    cf = ClusteringFrame()
    k = 100
    centroids, clustering = cf.kmeans(x, k, iterations=20)
    print(centroids)
    #visualize_dataframe(data)
    """
