# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# uv-nc_to_s-tif.py
# Created on: 2014-10-11 12:02:09.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

arcpy.env.overwriteOutput = True

# Local variables:
v_nc = "H:\\esm296-4f\\labs\\lab2\\raw\\uwnd.sig995.2013.nc"
u_nc = "H:\\esm296-4f\\labs\\lab2\\raw\\vwnd.sig995.2013.nc"
in_countries = "H:\\esm296-4f\\labs\\lab2\\raw\\World_EEZ_v8_2014.shp"
s_avg_tif = "H:\\esm296-4f\\labs\\lab2\\out\\s_avg.tif"
out_countries = "H:\\esm296-4f\\labs\\lab2\\lab2.gdb\\countries"
s_countries = "H:\\esm296-4f\\labs\\lab2\\lab2.gdb\\s_countries"

# loop over a range of values for j
for j in range(0, 365, 30):
    
    # assign values based on variable j
    s_001_tif = "h:\\esm296-4f\\labs\\lab2\\out\\s_%03d.tif" % j
    print s_001_tif
    
    u_001 = "u_%03d" % j
    s_001 = "in_memory\\s_%03d" % j
    v_001 = "v_%03d" % j
    s_001_tif = "H:\\esm296-4f\\labs\\lab2\\out\\s_%03d.tif" % j

    # Process: Make NetCDF Raster Layer
    arcpy.MakeNetCDFRasterLayer_md(v_nc, "uwnd", "lon", "lat", "u_%03d" % j, "", "time %03d" % j, "BY_INDEX")

    # Process: Make NetCDF Raster Layer (2)
    arcpy.MakeNetCDFRasterLayer_md(u_nc, "vwnd", "lon", "lat", "v_%03d" % j, "", "time %03d" % j, "BY_INDEX")

    # Process: Raster Calculator
    arcpy.gp.RasterCalculator_sa("SquareRoot( Square('%s') + Square('%s') )" % (u_001, v_001), s_001)

    # Process: Resample
    arcpy.Resample_management(s_001, s_001_tif, "0.25 0.25", "BILINEAR")


s_tifs = ["h:\\esm296-4f\\labs\\lab2\\out\\s_%03d.tif" % j for j in range(0, 365, 30)]

arcpy.gp.CellStatistics_sa(s_tifs, s_avg_tif, "MEAN", "DATA")

# Process: Copy Features
arcpy.CopyFeatures_management(in_countries, out_countries, "", "0", "0", "0")
# Process: Cell Statistics
arcpy.gp.CellStatistics_sa(s_tifs, s_avg_tif, "MEAN", "DATA")
# Process: Zonal Statistics as Table
arcpy.gp.ZonalStatisticsAsTable_sa(out_countries, "COUNTRY", s_avg_tif, s_countries, "DATA", "MIN_MAX_MEAN")
# Process: Join Field
arcpy.JoinField_management(out_countries, "COUNTRY", s_countries, "COUNTRY", "Min;Max;Mean")
