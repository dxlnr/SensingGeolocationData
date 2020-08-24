import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import geopandas as gpd
import descartes

from pathlib import Path
file = Path(__file__)
ROOT_PATH = file.parent.parent
STREET_PATH = ROOT_PATH.joinpath("israel_palestine_landscape")

def visualize_dataframe(df):
    '''
    Visualize the Geolocation dataframe which consists of "Latitude", "Longitude", "Altitude" and "Timestamp".
    :params df: pandas dataframe.
    '''
    # 2D-arrays from DataFrame
    x = np.linspace(df['Latitude'].min(), df['Latitude'].max(), len(df['Latitude']))
    y = np.linspace(df['Longitude'].min(), df['Longitude'].max(), len(df['Longitude']))

    x_, y_ = np.meshgrid(x, y)

    # Interpolate unstructured D-dimensional data.
    z2 = griddata((df['Latitude'], df['Longitude']), df['Altitude'], (x_, y_), method='cubic')

    # Ready to plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.title('Geolocation')

    plt.show()


def visualize_np_array(np_array):
    '''
    Visualize the Geolocation dataframe which consists of "Latitude", "Longitude", "Altitude" and "Timestamp".
    :params np_array: numpy array --- shape (X,2).
    '''
    fig = plt.figure()
    plt.title('Geolocation')
    plt.scatter(np_array[:,1], np_array[:,0])
    plt.show()


def vis_map_shp_data(dataframe, filename):
    '''
    Visualize the Geolocation dataframe which consists of "Latitude", "Longitude" on a given image that represents
    the landscape.
    :params dataframe: pandas dataframe.
    :params filename: name of the file that contains the street map --> .shp
    '''
    street_map = gpd.read_file(os.path.join(STREET_PATH, filename))
    fig, ax = plt.subplots(figsize=(20,20))
    street_map.plot(ax = ax)
    plt.show()

def vis_map_png_data(df, filename):
    '''
    Visualize the Geolocation dataframe which consists of "Latitude", "Longitude" on a given image that represents
    the landscape.
    :params df: pandas dataframe.
    :params filename: name of the file that contains the street map --> .png
    '''
    fig, ax = plt.subplots(1,1)
    png_map = plt.imread(os.path.join(STREET_PATH, filename))
    BBox = (df.Longitude.min(), df.Longitude.max(), df.Latitude.min(), df.Latitude.max())

    ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha= 0.2, c='b', s=10)
    ax.set_title('Plotting Spatial Data on Israel')
    ax.set_xlim(BBox[0],BBox[1])
    ax.set_ylim(BBox[2],BBox[3])

    ax.imshow(png_map, zorder=0, extent = BBox, aspect= 'equal')
    plt.show()
