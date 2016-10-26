geoplot
-------

A python library to plot shapely objects, combined with data sets.

Installation
============

Use pypi to install the latest version.

.. code:: bash

  pip3 install -e /path/to/your/clone/geoplotlib
  

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
   
