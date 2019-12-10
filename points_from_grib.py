
import numpy as np
from datetime import datetime, timedelta
import os
import re
import pandas as pd

# Detects the structure from current working directory, change if different
#home="/metdat/SOO/PlumeViewer/"
home = os.getcwd()

datadir= home + '/data/'
gribdir= datadir + 'NBM/2019110512/'
grib= gribdir + 'nbm.master'
locationfile = home + '/locations.csv'
output_path = datadir + 'plumes/'
#tmpfile = output + 'tmp.txt'
wgrib2path='/usr/bin/wgrib2'
# Time Script Started
startTime = datetime.now()




# ---- The following code provided by Nickolai Reimer - a.k.a the Python Wizard ----

# uses output from wgrib2 and passes it into a data frame
#  Need to have the list of locations in the order they were called in the -lon commands from wgrib2
def parse_to_dataframe(wgrib2_output, location_list):
    ##global output_path
    #with open(output_path + 'wgrib2.txt', 'w') as out_file:
    #    out_file.write(wgrib2_output)
    print("Reading wgrib2 output")
    parsed_data = []
    for line in wgrib2_output.strip().split('\n'):
        accum_suffix = ''
        accum_match = re.search("(\\d+)-(\\d+) hour", line)
        if accum_match is not None:
            accum_suffix = str(int(accum_match.group(2))-int(accum_match.group(1)))+'hr'
        accum_match = re.search("(\\d+)-(\\d+) day", line)
        if accum_match is not None:
            accum_suffix = str(int(accum_match.group(2))-int(accum_match.group(1)))+'dy'
        vt, field, surface, stat_type = re.search('vt\\=([^\\:]+)\\:([^\\:]+)\\:([^\\:]*)\\:[^\\:]*\\:([^\\:]*)\\:', line).groups()
        field += accum_suffix
        parsed_data.append([vt, '_'.join([x for x in [field, surface, stat_type] if x != ''])] + [float(x.replace('val=', '')) for x in re.findall('val\\=[^\\:]+', line)])
    return pd.DataFrame(parsed_data, columns=['ValidTime', 'Field'] + location_list)

# Pivots the data frame such that the rows are ValidTimes and the columns are model fields and writes a file for each unique location
# requested from wgrib2
def export_site_csv(full_data,output_path):
    #full_data.to_csv(output_path + "full_data.csv", index=False)
    for site in full_data.columns[2:]:
        print("Exporting " + site)
        full_data.pivot(index='ValidTime', columns='Field', values=site).reset_index().sort_values('ValidTime').to_csv(output_path+site+'.csv',index=False)



# file with lat,lon,locations , closestlat and closestlon are the location in the gribfile closest to the requested lat/lon
# this is pre-processed
df= pd.read_csv(locationfile, names = ["ID","City","State","Lat","Lon", "ClosestLat", "ClosestLon"], header=None)

rows= df.shape[0]
print("Lines in locationfile")
print(rows)

rows=10

# Limit number of location calls to wgrib2, system limitations limit the number/length of command line calls 
locationchunk=800

# if there are less rows than the requested locationchunk, adjust the location chunk
if rows <= locationchunk:
    locationchunk=rows
    print("Lines in location file are less than chunk --- adjusting chunk to:")
    print(locationchunk)



# Loop through the locationsfile locationchunck size at a time, capture output as dataframe




#print("Removing Temporary File if it exists")

#if os.path.exists(tmpfile):
#    os.remove(tmpfile)


line=0
# Loop line by line through the location dataframe
while line < rows:
    latloncommand=''
    location_list=[]
    i=0
    # Loop through a locationchunk size portion of the locations list
    while (i <= locationchunk) and (line < rows):
        # Make a list of all location IDs that will be processed in this chunk
        loc=str(df.loc[line,"ID"])
        location_list.append(loc)
        # Make a string of all lat/lon commands that will be passed to wgrib in this chunk
        latloncommand=latloncommand +' -lon ' + str(df.loc[line,"ClosestLon"]) + ' ' + str(df.loc[line,"ClosestLat"])
        i=i+1
        line=line+1

    # Call wgrib          
    command=wgrib2path + ' ' + grib + ' ' + " -verf " + latloncommand + ' -not ' + '"' +"(PWTHER|TSTM)"+'"' 
    #' ' + '-match "(TMP|WIND)"'

    wgrib2_output=os.popen(command).read()

    #print(wgrib2_output)

    print(location_list)
    
    export_site_csv(parse_to_dataframe(wgrib2_output, location_list),output_path)


endtime=(datetime.now() - startTime)
# Time script took to run
print("Time it took this script to run:", str(endtime) )
    
    


