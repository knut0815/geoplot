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
    def __init__(self, geom, bbox, **kwargs):
        self.geometries = geom
        self.bbox = bbox
        self._ax = kwargs.get('ax', plt.subplot(111))
        self.color = kwargs.get('color', None)
        self.cmapname = kwargs.get('cmapname', 'seismic')
        self.basemap = kwargs.get('basemap', self.create_basemap())
        self.data = kwargs.get('data')
        self.nancolor = kwargs.get('nancolor', 'grey')

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

    def select_color(self, colortype, cmap, n=None):
        if colortype == 'data':
            if np.isnan(self.data[n]):
                return self.nancolor
            else:
                return cmap(self.data[n])
        elif isinstance(colortype, float):
            return cmap(float)
        elif isinstance(colortype, str):
            return colortype
        elif isinstance(colortype, type(None)):
            return 'none'
        else:
            return self.color[n]

    def plot(self, ax=None, cmapname=None, cmap=None, linewidth=1,
             edgecolor='grey', facecolor=None, alpha=1):
        """Plot the geometries on the basemap using the defined colors

        Parameters:
        -----------
        ax : matplotlib.axis object
            An axis object for plots. Overwrites the self.ax attribute.
        cmapname : string
            Name of the color map from matplotlib (LINK!) (default: 'seismic')
        cmap : matplotlib colormap
            You can create you own colormap and pass it to the plot.
        linewidth : float
            Width of the lines.
        edgecolor : string, float or iterable
            Definition of the edge color. Can be an iterable with a color
            definition for each geometry, a string with one color for
            all geometries or a float to define one color for all geometries
            from the cmap.
        facecolor : string, float or iterable
            Definition of the face color. See edgecolor.
        alpha : float
            Level of transparency.
        """
        if ax is not None:
            self.ax = ax
        n = 0
        if facecolor is None:
            facecolor = self.color
        if edgecolor is None:
            edgecolor = self.color
        if cmapname is not None:
            self.cmapname = cmapname
        if self.data is not None:
            self.data = np.array(self.data)
        if cmap is None:
            cmap = plt.get_cmap(self.cmapname)
        for geo in self.geometries:
            vectors = self.get_vectors_from_postgis_map(geo)
            lines = LineCollection(vectors, antialiaseds=(1, ))
            lines.set_facecolors(self.select_color(facecolor, cmap, n))
            lines.set_edgecolors(self.select_color(edgecolor, cmap, n))
            lines.set_linewidth(linewidth)
            lines.set_alpha(alpha)
            self.ax.add_collection(lines)
            n += 1

    def draftplot(self, **kwargs):
        """Show a draft plot of the geometries.
        """
        self.ax = plt.subplot(111)
        plt.box(on=None)
        if self.data is not None:
            kwargs['facecolor'] = 'data'
            kwargs['edgecolor'] = 'data'
            self.draw_legend((0, 1), integer=False)
        self.plot(**kwargs)
        plt.tight_layout()
        plt.show()

    def create_basemap(self, projection='merc'):
        """Creates a very basic basemap: 'bbox': (x1, x2, y1, y2)

        If you want to use the power of basemap you can write your own basemap
        and pass it to you object
        """
        bm = Basemap(
            llcrnrlat=self.bbox[2], urcrnrlat=self.bbox[3],
            llcrnrlon=self.bbox[0], urcrnrlon=self.bbox[1],
            projection=projection)
        bm.drawcoastlines(linewidth=0)
        return bm

    def draw_legend(self, interval=(0, 1), legendlabel='Label', fontsize=15,
                    **kwargs):
        """Draw a typical legend.

        If you want to do something special you can write your own legend
         function in your app and use it instead.

        Parameters:
        -----------
        interval : tuple
            Defining the minimum and maximum value of the legend representing
            0 to 1 from the data set.
        """
        lcmap = kwargs.get('cmap', plt.get_cmap(self.cmapname))
        dataarray = np.clip(np.random.randn(250, 250), -1, 1)
        cax = self.ax.imshow(
            dataarray,
            interpolation=kwargs.get('interpolation', 'nearest'),
            vmin=kwargs.get('vmin', 0),
            vmax=kwargs.get('vmax', 1),
            cmap=lcmap)
        cax.set_alpha(kwargs.get('alpha', 1))
        cbar = self.basemap.colorbar(
            cax,
            location=kwargs.get('location', 'bottom'),
            pad=kwargs.get('pad', '5%'),
            extend=kwargs.get('extend', 'max'))
        cbar.set_label(legendlabel, size=fontsize)
        cbar.ax.tick_params(labelsize=fontsize)
        cbar.set_clim(kwargs.get('vmin', 0), kwargs.get('vmax', 1))

        def create_ticks(min_val, max_val, integer=False,
                         number_ticks=kwargs.get('number_ticks', 5)):
            tick_list = [min_val]
            for n in range(number_ticks - 2):
                tick_list.append((n + 1) * (max_val - min_val) /
                                 (number_ticks - 1) + min_val)
            tick_list.append(max_val)
            if integer:
                tick_list = [int(x) for x in tick_list]
            return tick_list
        if not kwargs.get('default_ticks', False):
            cbar.set_ticks(create_ticks(0, 1))
            cbar.set_ticklabels(
                kwargs.get('tick_list', create_ticks(
                    interval[0], interval[1], integer=kwargs.get(
                        'integer', False))))

    def draw_coordinate_system(self):
        """Draws parallels and meridians - still experimental
        """
        # Draw parallels and meridians
        self.basemap.drawparallels(
            np.arange(self.bbox[2], self.bbox[3], 3),
            labels=[1, 0, 0, 0], color='grey', dashes=[1, 0.1],
            labelstyle='+/-',
            linewidth=0.2)
        self.basemap.drawmeridians(
            np.arange(self.bbox[0], self.bbox[1], 3),
            labels=[0, 0, 0, 1], color='grey', dashes=[1, 0.1],
            labelstyle='+/-',
            linewidth=0.2)

    @property
    def ax(self):
        return self._ax

    @ax.setter
    def ax(self, new_ax, my_basemap=None):
        """Updates the basemap if the axis is updated.

        Arguments:
        ----------
        new_ax : matplotlib axis object
            New axis object.
        my_basemap: matplotlib basemap
            Pass you own basemap to use it instead.
        """
        self._ax = new_ax
        if my_basemap is None:
            self.basemap = self.create_basemap()


def postgis2shapely(postgis):
    geometries = list()
    for geo in postgis:
        geometries.append(wkt_loads(geo))
    return geometries
