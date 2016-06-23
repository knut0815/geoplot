import matplotlib.pyplot as plt
import numpy as np
from shapely.wkt import loads as wkt_loads
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap


class GeoPlotter:
    """
    Parameters:
    -----------
    geometries : list of shapely.geometry objects
        List of geometries to be plotted
    bbox : tuple
        Definition of a bounding box (x1, x2, y1, y2)

    Attributes:
    -----------
    ax : matplotlib.axis object
        An axis object for plots
    basemap : basemap object
        A basemap object from the matplotlib basemap extension. If not set
        a very basic basemap in a mercator projection will be created
    cmapname : string
        Name of the color map from matplotlib (LINK!) (default: 'seismic')
    color : string, float or iterable
        Definition of the plot color. Can be an iterable with a color
         definition for each geometry, a string with one color for
          all geometries or a float to define one color for all geometries
          from the cmap (default: blue).
    data : iterable
        Data set to define the color. Values must be between 0 an 1. Should
         be None (not defined) to use the color attribute


    """
    def __init__(self, geom, **kwargs):
        self.geometries = geom
        # 'bbox': (x1, x2, y1, y2)
        self.bbox = kwargs.get('bbox')
        self.basemap = kwargs.get('basemap', self.create_basemap())
        self.ax = kwargs.get('ax')
        self.data = kwargs.get('data')

    def create_vectors_multipolygon(self, multipolygon):
        """Create the vectors for MultiPolygons.
        """
        vectors = []
        for polygon in multipolygon:
            seg = []
            for coord in list(polygon.exterior.coords):
                seg.append(self.basemap(coord[0], coord[1]))
            vectors.append(np.asarray(seg))
        return vectors

    def create_vectors_polygon(self, polygon):
        """Create the vectors for Polygons.
        """
        vectors = []
        seg = []
        for coord in list(polygon.exterior.coords):
            seg.append(self.basemap(coord[0], coord[1]))
        vectors.append(np.asarray(seg))
        return vectors

    def create_vectors_multilinestring(self, multilinestring):
        """Create the vectors for MulitLineStrings.
        """
        vectors = []
        for linestring in multilinestring:
            seg = []
            for coord in list(list(linestring.coords)):
                seg.append(self.basemap(coord[0], coord[1]))
            vectors.append(np.asarray(seg))
        return vectors

    def create_vectors_linestring(self, linestring):
        """Create the vectors for LineStrings.
        """
        vectors = []
        seg = []
        for coord in list(list(linestring.coords)):
            seg.append(self.basemap(coord[0], coord[1]))
        vectors.append(np.asarray(seg))
        return vectors

    def get_vectors_from_postgis_map(self, mp):
        """Check for the geometry type and call the appropriate function
         to create the vectors
        """
        if mp.geom_type == 'MultiPolygon':
            vectors = self.create_vectors_multipolygon(mp)
        elif mp.geom_type == 'Polygon':
            vectors = self.create_vectors_polygon(mp)
        elif mp.geom_type == 'MultiLineString':
            vectors = self.create_vectors_multilinestring(mp)
        elif mp.geom_type == 'LineString':
            vectors = self.create_vectors_linestring(mp)
        else:
            vectors = None
            print(mp.geom_type)
            msg = "ERROR: So far only the following types are supported: "
            msg += "MultiPolygon, Polygon, MultiLineString, LineString"
            print(msg)
        return vectors

    def plot(self, ax=None):
        """Draw the geometries onto the map"""
        if ax is not None:
            self.ax = ax
        if self.ax is None:
            # error
            pass
        farbe = np.array(range(1, 793)) / 792
        n = 0
        cmap = plt.get_cmap('hsv')
        for mp in self.geometries:
            vectors = self.get_vectors_from_postgis_map(mp)
            lines = LineCollection(vectors, antialiaseds=(1, ))
            lines.set_facecolors(cmap(farbe[n]))
            # lines.set_facecolors(main_dt['geo_tables'][key]['facecolor'])
            lines.set_edgecolors('white')
            lines.set_linewidth(1)
            self.ax.add_collection(lines)
            n += 1

    def showplot(self):
        """Creates the basic plot object.
        """
        self.ax = plt.subplot(111)
        plt.box(on=None)
        self.plot()
        plt.tight_layout()
        plt.show()

    def create_basemap(self, projection='merc'):
        """Creates the basemap: 'bbox': (x1, x2, y1, y2)
        """
        bm = Basemap(
            llcrnrlat=self.bbox[2], urcrnrlat=self.bbox[3],
            llcrnrlon=self.bbox[0], urcrnrlon=self.bbox[1],
            projection=projection)
        bm.drawcoastlines(linewidth=0)
        return bm


def postgis2shapely(postgis):
    geometries = list()
    for geo in postgis:
        geometries.append(wkt_loads(geo[1]))
    return geometries
