#! /usr/bin/env python

"""TODO: Maybe add a docstring containing a long description

  This would double as something we could put int the `long_description`
  parameter for `setup` and it would squelch some complaints pylint has on
  `setup.py`.

"""

from setuptools import find_packages, setup

setup(name='geoplot',
      version='0.0.1',
      author='Uwe Krien',
      author_email='uwe.krien@rl-institut.de',
      description='Geoplot for the open energy modelling framework',
      packages=find_packages(),
      package_dir={'geoplot': 'geoplot'},
      install_requires=['shapely >= 1.5',
                        'matplotlib >= 1.4',
                        'basemap >= 0.1',
                        'numpy >= 1.7.0']
      )
