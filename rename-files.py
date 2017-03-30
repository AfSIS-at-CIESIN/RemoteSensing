#!/usr/bin/python
# renames AfSIS files for publication
# author: John Squires

import argparse, datetime, os

# create the help message and input options
parser = argparse.ArgumentParser(description="Renames AfSIS files for publication")
requiredNamed=parser.add_argument_group("required named arguments")
requiredNamed.add_argument("-d", "--dataset", choices=['albedo'],
							help="dataset to change", required=True)

# parse the input arguments and assign to variables
args = parser.parse_args()

#
# ALBEDO
#
if args.dataset == "albedo":
	now = datetime.datetime.now()
	lastyear=str(now.year -1)
	# albedo dataset dict that holds full paths of filenames to be changed and what to change it to"
	albedoDict = {r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_shortwave/outputs/reprojected/clipped/BSA_shortwaveAverage_laea_clipped.tif'
				  :"M43BSALT_200002_"+lastyear+"12.tif",
				  r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_shortwave/outputs/reprojected/clipped/BSA_shortwaveStdDev_laea_clipped.tif'
				  :"M43BSSLT_200002_"+lastyear+"12.tif",
				  r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_shortwave/outputs/reprojected/clipped/BSA_shortwaveVariance_laea_clipped.tif'
				  :"M43BSVLT_200002_"+lastyear+"12.tif",
				  r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_nir/outputs/reprojected/clipped/BSA_nirStdDev_laea_clipped.tif'
				  :"M43BNSLT_"+lastyear+"12.tif",
				  r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_nir/outputs/reprojected/clipped/BSA_nirVariance_laea_clipped.tif'
				  :"M43BNVLT_"+lastyear+"12.tif",
				  r'/data4/afsisdata/USGS_updates/albedo/outputs/Albedo_BSA_nir/outputs/reprojected/clipped/BSA_nirAverage_laea_clipped.tif'
				  :"M43BNALT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_BSA_vis/geotiffs/outputs/reprojected/clipped/BSA_visVariance_laea_clipped.tif'
				  :"M43BVVLT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_BSA_vis/geotiffs/outputs/reprojected/clipped/BSA_visStdDev_laea_clipped.tif'
				  :"M43BVSLT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_BSA_vis/geotiffs/outputs/reprojected/clipped/BSA_visAverage_laea_clipped.tif'
				  :"M43BVALT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_nir/outputs/reprojected/clipped/WSA_nirStdDev_laea_clipped.tif'
				  :"M43WNSLT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_nir/outputs/reprojected/clipped/WSA_nirVariance_laea_clipped.tif'
				  :"M43WNVLT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_nir/outputs/reprojected/clipped/WSA_nirAverage_laea_clipped.tif'
				  :"M43WNALT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_shortwave/outputs/reprojected/clipped/WSA_shortwaveStdDev_laea_clipped.tif'
				  :"M43WSSLT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_shortwave/outputs/reprojected/clipped/WSA_shortwaveVariance_laea_clipped.tif'
				  :"M43WSVLT_"+lastyear+"12.tif",
				  r'/data6/afsisdata/Albedo_WSA_shortwave/outputs/reprojected/clipped/WSA_shortwaveAverage_laea_clipped.tif'
				  :"M43WSALT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_WSA_vis/geotiffs/outputs/reprojected/clipped/WSA_visStdDev_laea_clipped.tif'
				  :"M43WVSLT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_WSA_vis/geotiffs/outputs/reprojected/WSA_visVariance_laea_clipped.tif'
				  :"M43WVVLT_"+lastyear+"12.tif",
				  r'/data1/afsisdata/MODIS/Albedo_MCD43A3/Albedo_WSA_vis/geotiffs/outputs/reprojected/WSA_visAverage_laea_clipped.tif'
				  :"M43WVALT_"+lastyear+"12.tif"
				  }

	for fileToChange,afsisName in albedoDict.iteritems():
		directory = os.path.dirname(fileToChange)
		afsisPath = directory+os.sep+afsisName
		try:
			os.rename(fileToChange, afsisPath)
			print "changed: {}".format(fileToChange)
			print "to: {}\n".format(afsisPath)
		except OSError as e:
			print "unable to change: {}".format(fileToChange)
			print "to: {}".format(afsisPath)
			print "{}\n".format(os.strerror(e.errno))








