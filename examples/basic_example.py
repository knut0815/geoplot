#!/usr/bin/python3
# -*- coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import geoplot
import os.path
import pickle
import pandas as pd
from shapely.geometry import Polygon
plt.style.use('ggplot')

# Create list set of example geometries
geom = list()
x2 = 13.3
y2 = 52.5
for x in range(10):
    for y in range (5):
        x1 = 13.3 + x / 10
        x2 = 13.4 + x / 10
        y1 = 52.5 + y / 10
        y2 = 52.6 + y / 10
        geom.append(
            Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]))

# Set bounding box
bbox = (13.3, x2, 52.5, y2)

# Create random data
data = np.random.rand(len(geom))

# Create plotter object
my_example = geoplot.GeoPlotter(geom, bbox, data=data)
my_example.draftplot()

# ************* 2nd example *************

# Create a dictionary to initialise the object.
geom = pickle.load(open(os.path.join('data', 'region.data'), 'rb'))
data = np.random.rand(len(geom))
bbox = (13.1, 13.76, 52.3, 52.7)

parameters = {'geom': geom,
              'bbox': bbox,
              'data': data,
              'cmapname': 'OrRd'}

second_example = geoplot.GeoPlotter(**parameters)

second_example.plot(ax=plt.subplot(121), linewidth=0)
second_example.draw_legend((0, 1), legendlabel="Intensity",
                           extend='neither')
plt.box(on=None)

# Create a sorted data set
second_example.data = np.array(range(len(geom))) / len(geom)
second_example.cmapname = 'winter'
second_example.plot(ax=plt.subplot(122), edgecolor='white')
second_example.draw_legend((3, 50), integer=True, legendlabel="Level [m]",
                           extend='min')

plt.tight_layout()
plt.box(on=None)
plt.show()

# ************* 3rd example *************
# Plot an overview and zoom into in a second plot
parameters = {'geom': pickle.load(open(os.path.join('data', 'plr.data'), 'rb')),
              'bbox': (13.1, 13.76, 52.3, 52.7),
              'data': np.random.rand(453)}

third_example = geoplot.GeoPlotter(**parameters)
third_example.plot(cmapname='cool', linewidth=0)
third_example.draw_legend(location='right', tick_list=[0, 1, 10, 100, 1000],
                          legendlabel="Coolness factor in Berlin")

plt.tight_layout()
plt.box(on=None)
plt.show()

# Zoom into the plot
third_example.bbox = (13.4, 13.6, 52.45, 52.55)
third_example.plot(ax=plt.subplot(111), cmapname='cool', linewidth=0)
third_example.draw_legend(location='right', tick_list=[0, 1, 10, 100, 1000],
                          legendlabel="Coolness factor in Berlin")
plt.tight_layout()
plt.box(on=None)
plt.show()

# ************* 4th example *************
# Plot different Maps in one plot. Use csv files with geometries in the
# wkt-format (well-known-text).

my_df = pd.read_csv(os.path.join('data', 'onshore.csv'))
onshore = geoplot.postgis2shapely(my_df.geom)

fourth_example = geoplot.GeoPlotter(onshore, (3, 16, 47, 56))
fourth_example.plot(facecolor='#badd69', edgecolor='white')

fourth_example.geometries = geoplot.postgis2shapely(
    pd.read_csv(os.path.join('data', 'offshore.csv')).geom)
fourth_example.plot(facecolor='#a5bfdd', edgecolor='white')

fourth_example.geometries = pickle.load(
    open(os.path.join('data', 'region.data'), 'rb'))
fourth_example.plot(facecolor='#aa0000', edgecolor='#aa0000')

plt.tight_layout()
plt.box(on=None)
plt.show()

# ************* 5th example *************
my_df = pd.read_csv(os.path.join('data', 'lines.csv'))
geom = geoplot.postgis2shapely(my_df.geom)
fifth_example = geoplot.GeoPlotter(geom, (-12, 24, 36, 61))
fifth_example.basemap.resolution = 'f'
fifth_example.basemap.shadedrelief()
fifth_example.basemap.drawcountries(color='white')
fifth_example.plot(edgecolor='#4d55ba', linewidth=2, alpha=0.6)
plt.tight_layout()
plt.box(on=None)
plt.show()
