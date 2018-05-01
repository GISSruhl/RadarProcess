# RadarProcess

This script is a piece of my Master's Thesis for USC. It will eventually be wrapped in an Alteryx macro.  Currently, it accepts a
list of NEXRAD radar files, filters out those using the Clean Air Mode Volume Collection Protocol, then converts them to shapefiles, one each for the Reflectivity and Velocity attributes.


### Dependencies
**[ARM-DOE Py_ART:](https://github.com/ARM-DOE/pyart)** This repository contains all the functions used to process the radar files and create the geoTIFFs


**[OSGeo GDAL:](https://github.com/OSGeo/gdal)** This repository is used for geographic conversions. Specifically from geoTIFF to shapefile.
