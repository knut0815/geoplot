geoplot
-------

A python library to plot shapely objects, combined with data sets.

Installation
============

Use pypi to install the latest version. It is recommended to install basemap first.

.. code:: bash

  pip install git+https://github.com/matplotlib/basemap.git
  pip install git+https://github.com/rl-institut/geoplot.git
  
If your geos version is too old for the newest version of shapely, you can install an older one.

.. code:: bash

  pip install shapely==1.4.3
  
If you want to run the examples you have to install pandas.

.. code:: bash

  pip install pandas

Gallery
=======

The code of the following maps can be found in the `example file <https://github.com/rl-institut/geoplot/blob/master/examples/basic_examples.py>`_.

Plotting a map based on Berlin's planing regions (random data)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
.. image:: docs/gallery/berlin_planing_regions_all.png
   
   
Zooming into the map from above
++++++++++++++++++++++++++++++++

.. image:: docs/gallery/berlin_planing_regions_zoom.png

Plotting two maps in one figure
+++++++++++++++++++++++++++++++++    
.. image:: docs/gallery/berlin_districts.png

Plotting different maps into one figure using specific colours
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(offshore=blue, onshore=green, city=red)
  
.. image:: docs/gallery/germany_grid_regions_plus_berlin.png

Plotting the electrical output of wind (left) and pv (right) power plants
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

(Germany, 2012, using the coastDat2 weather data set)
 
.. image:: docs/gallery/pv_and_wind_power_feedin.png

Plotting lines onto a relief map from matplotlib basemap
++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
.. image:: docs/gallery/european_substitute_grid.png
   
