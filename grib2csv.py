#!/usr/bin/python

# Decodes grib files at METAR locations and produces csv file for use in WAVE 1-D plume viewer


import os
import csv
import subprocess
import re
from datetime import datetime, timedelta
import pandas as pd
home="/metdat/SOO/PlumeViewer/"

datadir= home + 'data/'
gribdir= datadir + 'NBM/2019110512/'
grib= gribdir + 'nbm.master'
locationfile = home + 'locations.csv'
datafile= home + 'test.txt'

# Time Script Started
startTime = datetime.now()




# Get # of unique parameters



matchcommands='"'+"(WIND|GUST|TMP|WDIR|APCP|PTYPE|DPT|VIS|CAPE|PWTHER|ASNOW|RH|TMIN|TMAX|TSTM|MAXRH|MINRH|MIXHT)"+'"'
locationcommands=[]

# Limit number of location calls to wgrib2, system limitations limit the number/length of command line calls 
locationchunk=800

# Number of lines in locations file
lines = 0


df= pd.read_csv(locationfile, index_col=0, names = ["ID","City","State","Lat","Lon"])
rows= df.shape[0]
print(rows)


quit()



with open(locationfile, "r") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		i=i+1
		stationid=row[0]
		station=row[1]
		state=row[2]
		lat=row[3]
		lon=row[4]
		location=" -lon " + lon + ' ' + lat
		locationcommands.append(location)
for line in open(locationfile):
	lines += 1

	
	
# Loop through lines


i=0
# Loop through location file calling wgrib2 as many times as needed given the locationchunk
#
#		if i == locationchunk:
#			break

#locationcommands=''.join(locationcommands)		

# Call wgrib2
#command="wgrib2 " + grib + ' ' + "-match " + matchcommands + ' ' + locationcommands + " -verf -ext_name" + " > " + datafile 





#command="wgrib2 " + grib + locationcommands + " -verf -ext_name" + " > " + datafile 

#command="/metdat/WAVE/data/scripts/bin/wgrib2 " + grib + ' ' + " -verf -ext_name" + " > " + datafile 

#print(command)
#os.system(command)


#args=command.split()
#print(args)
#subprocess.call(args, shell=True)

exit
#out=os.popen(command)
#for row in out:
#			if flag == 1:
#				break
#	line = re.split("[:,]", row )
#	#print(line)
#	value=line[4]
#	vt=line[5]
#	vt=vt[3:13]
			#vt_epoch=datetime.strptime(vt,"%Y%m%d%H").strftime('%s')
#	value=value[4:14]
#	var=line[10]
#	print(vt,var,value)		
		
#		print(locationcommands)
#print(len(locationcommands))
endtime=(datetime.now() - startTime)
# Time script took to run
print("Time it took this script to run:", str(endtime) )