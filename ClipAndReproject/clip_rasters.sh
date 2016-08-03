#!/bin/bash
# clip_rasters.sh
# written by: Kimberly Peng, 
# modified by: John Squires
# Clips rasters for geographic and lambert azimuthal equal area geotiffs.

#Sample Usage
#/data4/afsisdata/IRI_MODIS/scripts/./clip_rasters.sh /data4/AfSIS2tifs/SRTM/SRTM_AfricaClip_LAEA /data4/afsisdata/IRI_MODIS/scripts/test 30000 laeaKPtemp trmm

usage()
{
cat << EOF
USAGE: $0 options

This script clips geotiffs to a clip mask.
Can be used for geographic and lambert azimuthal equal area geotiffs.

OPTIONS:
   -h      Show this message
   -c      Directory containing clip masks (required)
   -i      Input directory of geotiffs to be clipped (required)
   -l      GRASS location (required)
   -m      GRASS mapset (required)
   -r      Resolution of data in meters (required)
             example -r 500 (for 500 meter resolution)
EOF
}

# declare globals and assign variables through getopts
ClipDir=
InputDir=
Resolution=
location=
mapset=

while getopts “hc:i:l:m:r:” OPTION
do
    case $OPTION in
    	c) ClipDir=$OPTARG
            ;;
        h) usage
            exit 1
            ;;
        i) InputDir=$OPTARG
			;;
		l) location=$OPTARG
			;;
		m) mapset=$OPTARG
			;;
		r) Resolution=$OPTARG
			;;	
        ?) usage
           exit
           ;;
     esac
done

# 5 required arguments, check that they were provided
if [[ -z "$ClipDir" ]] || [[ -z "$InputDir" ]] || [[ -z "$location" ]] || \
   [[ -z "$mapset" ]] || [[ -z "$Resolution" ]]; then
	printf '\nERROR: You need to supply the flags and values for each required argument.\n'
	usage
	exit 1
fi

#####Start grass environment#####
#some settings:
TMPDIR=/tmp

# path to GRASS binaries and libraries:
export GISBASE=/usr/lib/grass64

#Create temporary mapset with WIND parameter
mkdir /data3/grassdata/$location/$mapset
cp /data3/grassdata/$location/PERMANENT/WIND /data3/grassdata/$location/$mapset

# generate GRASS settings file:
# the file contains the GRASS variables which define the LOCATION etc.
echo "GISDBASE: /data3/grassdata
LOCATION_NAME: $location
MAPSET: $mapset
" > $TMPDIR/.grassrc6_modis$$

# path to GRASS settings file:
export GISRC=$TMPDIR/.grassrc6_modis$$

# first our GRASS, then the rest
export PATH=$GISBASE/bin:$GISBASE/scripts:$PATH
#first have our private libraries:
export LD_LIBRARY_PATH=$GISBASE/lib:$LD_LIBRARY_PATH

# use process ID (PID) as lock file number:
export GIS_LOCK=$$

#####Import clip file and set as mask#####
#change to the directory containing the clip file
cd $ClipDir

#add meter to resolution so that 500 AND 5000 aren't found with * operator
Resolution+="m"

clipfile=$(ls *"$Resolution"*)
echo $clipfile
r.in.gdal input=$ClipDir/$clipfile output=$clipfile
r.mask -o input=$clipfile@"$mapset"
g.region rast=$clipfile@"$mapset"

#####Import geotiffs to clip#####
#change to directory containing the inputs to export
cd $InputDir

#creates a directory in the Input Directory to store the clipped layers
mkdir $InputDir/clipped
chmod -R 775 $InputDir/clipped

#loops through all the files in the Input Directory
for file in *.tif
do
	#imports files
	echo $file
	newName=$(echo $file | sed 's/.tif//')
	r.in.gdal input=$InputDir/$file output=$newName

	#export clipped file
	r.out.gdal input=$newName@"$mapset" output=$InputDir/clipped/"$newName"_clipped.tif
	chmod 775 $InputDir/clipped/"$newName"_clipped.tif
done