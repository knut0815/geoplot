#!/usr/bin/python3
# -*- coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import geoplot
import pickle
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

# Create a dictionary using the data from above

parameters = {'geom': geom,
              'bbox': bbox,
              'data': data,
              'cmapname': 'OrRd'}

second_example = geoplot.GeoPlotter(**parameters)

second_example.plot(ax=plt.subplot(121))
second_example.draw_legend((0, 1), legendlabel="Intensity",
                           extend='neither')

# Create a sorted data set
second_example.data = np.array(range(len(geom))) / len(geom)
second_example.cmapname = 'winter'
second_example.plot(ax=plt.subplot(122))
second_example.draw_legend((3, 50), integer=True, legendlabel="Height [m]",
                           extend='min')

plt.tight_layout()
plt.show()

# ************* 3rd example *************

parameters = {'geom': pickle.load(open('test.data', 'rb')),
              'bbox': (13.1, 13.76, 52.3, 52.7),
              'data': np.random.rand(12)}

third_example = geoplot.GeoPlotter(**parameters)
third_example.plot(cmapname='cool')
third_example.draw_legend((0, 4), integer=True, location='right',
                          legendlabel="Coolness factor in Berlin")

plt.tight_layout()
plt.show()
