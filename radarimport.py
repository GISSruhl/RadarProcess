# Import libraries
import pyart
from osgeo import gdal, ogr, osr
import matplotlib.pyplot as plt
from os import path

countfiles = 0
countprocessedfiles = 0
errorfiles = 0

rootdir = r'C:\ProgramData\Alteryx\Engine'
for root, dirs, files in os.walk(rootdir):
    for file in files:
        if file == 'RadarList': # use your filename here without file type extension
            filepath = os.path.join(root, file) 
            fileroot = root
                
with open(filepath, "r") as file:
    filelist = file.readlines()
    for line in filelist:

        print(line)
        # Find directory for NEXRAD files
        radarname = line[:-1]
        radarpath = root
        fullpath = path.join(radarpath, radarname)
        try:
            radar = pyart.io.read_nexrad_archive(fullpath)
            # print("Radar Fields \n",radar.fields)
            vcppatt = radar.metadata["vcp_pattern"]
            # print("VCP Pattern \n", vcppatt)
            countfiles += 1
            if vcppatt == 32 or vcppatt == 31:
                print("Select radar, it's good for finding birds.")
                countprocessedfiles += 1
                # compute noise
                grid_shape = (1, 241, 241)
                grid_limits = ((2000, 2000), (-123000.0, 123000.0), (-123000.0, 123000.0))
                # field = radar.get_field (0, 'reflectivity')
                grid = pyart.map.grid_from_radars(radar, grid_shape, grid_limits, 'map_to_grid')

                tiffpath = root
                tiffname = radarname + "_v.tif"
                fulltiffpathv = path.join(tiffpath, tiffname)
                pyart.io.output_to_geotiff.write_grid_geotiff(grid, fulltiffpathv, 'velocity')

                tiffname = radarname + "_r.tif"
                fulltiffpathr = path.join(tiffpath, tiffname)
                pyart.io.output_to_geotiff.write_grid_geotiff(grid, fulltiffpathr, 'reflectivity')


                # GeoTiff to Vector then export as GeoJSON
                gdal.UseExceptions()
                sourceraster = gdal.Open(fulltiffpathv)

                # rastercount = sourceraster.GetRasterCount()
                # print("Raster Count\n",rastercount)
                rasterband = sourceraster.GetRasterBand(1)

                outlayerpath = r"G:\RadarData\Testout"
                outlayername = radarname + "_v.shp"
                outlayer = path.join(outlayerpath, outlayername)

                shapedriver = ogr.GetDriverByName("ESRI Shapefile")

                datasource = shapedriver.CreateDataSource(outlayer)

                # get proj from raster
                srs = osr.SpatialReference()
                srs.ImportFromWkt(sourceraster.GetProjectionRef())
                # create layer with proj
                outlayershp = datasource.CreateLayer(outlayer, srs)

                newfield = ogr.FieldDefn('Velocity', ogr.OFTInteger)
                outlayershp.CreateField(newfield)

                gdal.Polygonize(rasterband, None, outlayershp, 0, [], callback=None)

                # GeoTiff to Vector then export as GeoJSON
                gdal.UseExceptions()
                sourceraster = gdal.Open(fulltiffpathr)

                # rastercount = sourceraster.GetRasterCount()
                # print("Raster Count\n",rastercount)
                rasterband = sourceraster.GetRasterBand(1)

                outlayername = radarname + "_r.shp"
                outlayer = path.join(outlayerpath, outlayername)

                shapedriver = ogr.GetDriverByName("ESRI Shapefile")

                datasource = shapedriver.CreateDataSource(outlayer)

                # get proj from raster
                srs = osr.SpatialReference()
                srs.ImportFromWkt (sourceraster.GetProjectionRef())
                # create layer with proj
                outlayershp = datasource.CreateLayer(outlayer, srs)

                newfield = ogr.FieldDefn('Reflectivity', ogr.OFTInteger)
                outlayershp.CreateField(newfield)

                gdal.Polygonize(rasterband, None, outlayershp, 0, [], callback=None)

        except:
            errorfiles += 1
            print("Unknown compression type for ", line)
            pass



print("End Test")
print(countprocessedfiles, " out of ", countfiles, " processed with ", errorfiles, " file read errors")
file.close()
