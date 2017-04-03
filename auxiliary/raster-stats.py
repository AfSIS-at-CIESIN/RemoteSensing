#!/usr/bin/python
# processes a directory of geotiffs and outputs a cvs file with basic statistics
# author: John Squires

import argparse, csv, datetime, glob, os
from osgeo import gdal

gdal.UseExceptions()

# create the help message and input options
parser = argparse.ArgumentParser(description="Processes a DIRECTORY of GeoTIFFs and outputs a csv file "\
                                 "cointaining basic statistics")
parser.add_argument("-m", "--match", help="string to match in geoTIFF filenames")
requiredNamed=parser.add_argument_group("required named arguments")
requiredNamed.add_argument("-d", "--directory", help="full directory path of files to mosaic", required=True)
#requiredNamed.add_argument("-f", "--firstmatch", help="string to match in first file to mosaic", required=True)
#equiredNamed.add_argument("-s", "--secondmatch", help="string to match in file to be mosaiced with firstmatch", required=True)

# parse the input arguments and assign to variables
args = parser.parse_args()

outfile = "rasterStats.csv"
headings = ['CreationDate','FileName','Resolution','NoData','Min','Max','Mean','StdDev','FilePath']
file_exists = os.path.isfile(outfile)

# create list of files to work with
if args.match:
	files_matched=glob.glob(args.directory+os.sep+'*'+args.match+'*.tif')
else:
	files_matched=glob.glob(args.directory+os.sep+'*.tif')

if not files_matched:
	print "no files to process"
	exit()


# open a file to write to
with open(outfile,'ab') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=headings, dialect='excel')
	if not file_exists:
		writer.writeheader()  # file doesn't exist yet, write a header
	# filename, location
	for f in files_matched:
			print "processing {}".format(os.path.basename(f))
			# create data dictionary to store raster information
			rstats = {}
			# get file creation time
			ctime = os.path.getctime(f)
			# convert to human readable (we just need YYYYMMDD)
			rstats['CreationDate'] = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
			rstats['FileName'] = os.path.basename(f)
			src = gdal.Open(f)
			# get resolution
			resolution = src.GetGeoTransform()
			rstats['Resolution'] = resolution[1]
			# assume only one band and get it for band statistics
			src_band = src.GetRasterBand(1)
			rstats['NoData'] = src_band.GetNoDataValue()
			# get statistics
			stats = src_band.GetStatistics(False,True)
			rstats['Min'] = round(stats[0],3)
			rstats['Max'] = round(stats[1],3)
			rstats['Mean'] = round(stats[2],3)
			rstats['StdDev'] = round(stats[3],3)
			rstats['FilePath'] = os.path.abspath(os.path.dirname(f))
			writer.writerow(rstats)
