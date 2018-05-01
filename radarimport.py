"""
TODO: Investigate the cartesian_to_geographic function in pyart.core to convert cartesian coordinates

"""

# Import libraries
import pyart
import gdal_polygonize as gdalpoly
import matplotlib.pyplot as plt

# Find directory for NEXRAD files

radar = pyart.io.read_nexrad_archive("G:\RadarData\KFFC20160811_150625_V06")

# print("Lat/Long"
#      "n", radar.latitude["data"], ",", radar.longitude["data"])
# print("Sweep Mode\n", radar.sweep_mode)
# print("Sweep Number\n", radar.sweep_number)

# Only get sweeps below .5 degrees elevation
sweepdict = {}
sweeplist = radar.sweep_number['data']
for sweep in sweeplist:
    sweepelevation = radar.get_elevation(sweep)
    if sweepelevation[0] < .5:
        sweepdict[sweep] = sweepelevation[0]
    else:
        pass
print("Sweeps below .5 degrees \n", sweepdict)

# Get radar gates for converting to coordinates
gates = radar.get_gate_x_y_z (0, False, True)
print("Gates\n", gates)

# Get Azimuth

azimuth = radar.get_azimuth (0)
print("Azimuth \n", azimuth)

# print("Radar Fields \n",radar.fields)
print("VCP Pattern \n", radar.metadata["vcp_pattern"])
vcppatt = radar.metadata["vcp_pattern"]
if vcppatt == 32 or vcppatt == 31:
    print("Select radar, it's good for finding birds.")

# radarplot = pyart.graph.RadarDisplay(radar)
# print("Radar Plot\n", radarplot.loc)
# print("\n\n\n\n")
# display = pyart.graph.RadarDisplay(radar)
# fig = plt.figure(figsize=(6,5))
#
# ax = fig.add_subplot(111)
# display.plot('velocity', 0, title = 'NEXRAD Velocity',
#              vmin=-1, vmax=1, colorbar_label='', ax=ax)
# display.plot_range_ring(radar.range['data'][-1]/ 1200., ax=ax)
# display.set_limits(xlim=(-400,400), ylim=(-400, 400), ax=ax)
# plt.show()
# drawradar = pyart.core.antenna_to_cartesian(radar.range, radar.get_azimuth(1), radar.get_elevation)
# print(drawradar)


# Begin Radar cleaning

# Find gating objects (things that block radar signatures like trees or mountains) using
# pyart.correct.find_objects

# pyart.retreive.kdp_maesaka to get differential phase.  Noisy differential phase is a sign of
# biological activity


# compute noise
grid_shape = (1, 241, 241)
grid_limits = ((2000, 2000), (-123000.0, 123000.0), (-123000.0, 123000.0))
field = radar.get_field(0, 'reflectivity')
grid = pyart.map.grid_from_radars(radar, grid_shape, grid_limits, 'map_to_grid')
print(grid)

pyart.io.output_to_geotiff.write_grid_geotiff(grid, r'G:\RadarData\Testout\test.tif', 'velocity')

# GeoTiff to Vector then export as GeoJSON
gdal.UseExceptions()
sourceraster = gdal.Open(r'G:\RadarData\Testout\test.tif')

rasterband = sourceraster.GetRasterBand()