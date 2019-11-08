# Creates a list of locations for plume viewer
# Combines a list of METAR/FAA sites, with a RAWS list, and user supplemented locations
 

home="/metdat/SOO/PlumeViewer/"
metar_locations= home + "METAR_stations.txt"
locationfile= home + "locations.csv"


# ----- Processing METAR_stations file into CONUS METAR sites

excludestates=['AK', 'HI', 'PR', 'UM', 'GU', 'MH']


# For each state listed, look for METAR sites
# at those METAR sites print out a csv
# open the 

with open(locationfile, "w+") as file:

    with open(metar_locations) as f:
        content = f.readlines()
        for i in content:
            stateid=i[0:2]
#        print stateid
#            
# For CONUS states in the US, select each METAR site
# X denotes METAR site

#

            if ( i[81:83] == 'US' ) and ( stateid not in excludestates ) and ( i[62:63] == 'X' ):
             
                station=i[3:19]
                stationid=i[20:24]
                lat=i[39:41]+'.'+i[42:44]
                lon='-'+i[47:50]+'.'+i[51:53]
                file.write(stationid + "," + station + "," + stateid + "," + lat + "," + lon + '\n')

        
#for state in states:
#
#    print(state)
file.close()
