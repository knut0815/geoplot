# -*- coding: utf-8 -*-
'''
BaseMap example based on by tutorial 10 by geophysique.be
'''

from oemof import db
import sys
import numpy as np
import matplotlib.pyplot as plt
from shapely.wkt import loads as wkt_loads
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap


def execute_read_db(dic, db_string):
    '''
    Executes a sql-string and returns a tuple
    '''
    return db.connection().execute(db_string).fetchall()


def fetch_geometries(main_dt):
    '''
    Reads the geometry and the id of all given tables and writes it to the
    'geom'-key of each branch of the data tree.
    '''
    sql_str = '''
        SELECT {id_col}, ST_AsText(
            ST_SIMPLIFY({geo_col},{simp_tolerance}))
        FROM {schema}.{table}
        WHERE "{where_col}" {where_cond}
        ORDER BY {id_col} DESC;'''

    for key in list(main_dt['geo_tables'].keys()):
        main_dt['geo_tables'][key]['geom'] = execute_read_db(
            main_dt, sql_str.format(**main_dt['geo_tables'][key]))


def db_connection():
    'Definition of the database connection'
    main_dt = {
        'db': 'name_of_db',  # name of your database
        'ip': 'localhost',  # ip of the database or 'localhost'
        'port': '5432',
        'password': 'pass',
        'user': 'username'}
    return main_dt


def map_definition(main_dt):
    'Definition of the maps'
    main_dt['geo_tables'] = {}

    # # Germany off-shore regions
    # main_dt['geo_tables']['de_offshore'] = {
    #     'table': 'deu3_21',  # name of the table
    #     'geo_col': 'geom',  # name of the geometry column
    #     'id_col': 'region_id',  # name of the geo-id column
    #     'schema': 'deutschland',  # name of the schema
    #     'simp_tolerance': '0.01',  # simplification tolerance (1)
    #     'where_col': 'region_id',  # column for the where-condition
    #     'where_cond': '> 11018',  # condition for the where-condition
    #     'facecolor': '#a5bfdd'   # color of the polygon (blue)
    #     }

    # # Germany on-shore regions
    # main_dt['geo_tables']['de_onshore'] = {
    #     'table': 'deu3_21',
    #     'geo_col': 'geom',
    #     'id_col': 'region_id',
    #     'schema': 'deutschland',
    #     'simp_tolerance': '0.01',
    #     'where_col': 'region_id',
    #     'where_cond': '< 11019',
    #     'linewidth': 1,
    #     'facecolor': None
    #     }

    # CoastDat2 grid for the Germany 21 region
    main_dt['geo_tables']['de_grid'] = {
        'table': 'de_grid',
        'geo_col': 'geom',
        'id_col': 'gid',
        'schema': 'coastdat',
        'facecolor': 'red',
        'simp_tolerance': '0.01',
        'where_col': 'gid',
        'where_cond': '> 0',
        'linewidth': -0.1,
        'alpha': 0.5,
        'color_map': 'seismic'
        }

def box_definition(main_dt):
    'Definition of the bounding box'
    main_dt['x1'] = 3
    main_dt['x2'] = 16.
    main_dt['y1'] = 47.
    main_dt['y2'] = 56


def create_vectors_multipolygon(main_dt, multipolygon):
    'Create the vectors for MultiPolygons'
    vectors = []
    for polygon in multipolygon:
        seg = []
        for coord in list(polygon.exterior.coords):
            seg.append(main_dt['m'](coord[0], coord[1]))
        vectors.append(np.asarray(seg))
    return vectors


def create_vectors_polygon(main_dt, polygon):
    'Create the vectors for Polygons'
    vectors = []
    seg = []
    for coord in list(polygon.exterior.coords):
        seg.append(main_dt['m'](coord[0], coord[1]))
    vectors.append(np.asarray(seg))
    return vectors


def create_vectors_multilinestring(main_dt, multilinestring):
    'Create the vectors for MulitLineStrings'
    vectors = []
    for linestring in multilinestring:
        seg = []
        for coord in list(list(linestring.coords)):
            seg.append(main_dt['m'](coord[0], coord[1]))
        vectors.append(np.asarray(seg))
    return vectors


def create_vectors_linestring(main_dt, linestring):
    'Create the vectors for LineStrings'
    vectors = []
    seg = []
    for coord in list(list(linestring.coords)):
        seg.append(main_dt['m'](coord[0], coord[1]))
    vectors.append(np.asarray(seg))
    return vectors


def get_vectors_from_postgis_map(main_dt, mp):
    '''
    Check for the geometry type and
    call the appropriate function to create the vectors
    '''
    if mp.geom_type == 'MultiPolygon':
        vectors = create_vectors_multipolygon(main_dt, mp)
    elif mp.geom_type == 'Polygon':
        vectors = create_vectors_polygon(main_dt, mp)
    elif mp.geom_type == 'MultiLineString':
        vectors = create_vectors_multilinestring(main_dt, mp)
    elif mp.geom_type == 'LineString':
        vectors = create_vectors_linestring(main_dt, mp)
    else:
        print(mp.geom_type)
        sys.exit(
            "ERROR: So far only (multi-)polygons and lines are supported.")
    return vectors


def create_geoplot(main_dt, key):
    """Draw the geometries onto the map"""
    farbe = np.array(range(1, 793)) / 792
    n = 0
    cmap = plt.get_cmap('hsv')
    for mp in main_dt['geo_tables'][key]['geom']:
        vectors = get_vectors_from_postgis_map(main_dt, wkt_loads(mp[1]))
        lines = LineCollection(vectors, antialiaseds=(1, ))
        lines.set_facecolors(cmap(farbe[n]))
        # lines.set_facecolors(main_dt['geo_tables'][key]['facecolor'])
        lines.set_edgecolors('white')
        lines.set_linewidth(1)
        main_dt['ax'].add_collection(lines)
        n += 1


def create_plot(main_dt):
    'Creates the basic plot object.'
    main_dt['ax'] = plt.subplot(111)
    plt.box(on=None)


def create_basemap(main_dt):
    'Creates the basemap.'
    main_dt['m'] = Basemap(
        resolution='i', epsg=None, projection='merc',
        llcrnrlat=main_dt['y1'], urcrnrlat=main_dt['y2'],
        llcrnrlon=main_dt['x1'], urcrnrlon=main_dt['x2'],
        lat_ts=(main_dt['x1'] + main_dt['x2']) / 2)
    main_dt['m'].drawcoastlines(linewidth=0)


def main():
    import time
    start = time.time()
    print("Using Python {0}.{1}".format(
        sys.version_info.major, sys.version_info.minor))
    'main function'
    # Definition of database connection
    main_dt = db_connection()

    # Definition of the maps
    map_definition(main_dt)

    # Definition of the bounding box
    box_definition(main_dt)

    # Retrieve geometries from database
    fetch_geometries(main_dt)

    # Create basic plot
    create_plot(main_dt)

    # Create Basemap
    create_basemap(main_dt)

    # Draw geometries
    for key in list(main_dt['geo_tables'].keys()):
        create_geoplot(main_dt, key)
    print(time.time() - start)

    # Show plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
