import os
import pygrib
import numpy as np
# Creates a list of locations for plume viewer
# Combines a list of METAR/FAA sites, with a RAWS list, and user supplemented locations
 

home = os.getcwd()
metar_locations= home + "/METAR_stations.txt"
locationfile= home + "/locations.csv"
datadir= home + '/data/'
gribdir= datadir + 'NBM/2019110512/'
grib= gribdir + 'nbm.small'

# ----- Processing METAR_stations file into CONUS METAR sites

excludestates=['AK', 'HI', 'PR', 'UM', 'GU', 'MH']


# For each state listed, look for METAR sites
# at those METAR sites print out a csv
# open the 

grbs= pygrib.open(grib)
grb=grbs.message(1)
lats,lons = grb.latlons()

locationInfo=[]
LAT=[]
LON=[]

with open(locationfile, "w+") as file:

    with open(metar_locations) as f:
        content = f.readlines()
        for i in content:
            stateid=i[0:2]
#        print stateid
#            
# For CONUS states in the US, select each METAR site
# X denotes METAR site

            if ( i[81:83] == 'US' ) and ( stateid not in excludestates ) and ( i[62:63] == 'X' ):
             
                station=i[3:19]
                stationid=i[20:24]
                lat=float(i[39:41]+'.'+i[42:44])
                lontemp=i[47:50]+'.'+i[51:53]
                lon=lontemp.lstrip("0")
                lon=float(lon)*-1

                # Find what the closest lat,lon from grib file is for each lat lon
                #LAT.append(lat)
                #LON.append(lon)

                abslat = np.abs(lats-lat)
                abslon = np.abs(lons-lon)
                # Absolute difference between the two


                c = np.maximum(abslon,abslat)
                # Minimum distance = closest point
                x,y = np.where( c == np.min(c))

                # Grid values at location
                closestlat = lats[x[0],y[0]]
                closestlon= lons[x[0],y[0]]
                print(lat,closestlat)
                locationInfo.append([stationid,station,stateid,lat,lon, closestlat,closestlon])
                file.write(stationid + "," + station + "," + stateid + "," + str(lat) + "," + str(lon) + ',' + str(closestlat) + ',' + str(closestlon) +'\n')



#LAT=np.asarray(LAT, dtype=np.float32)
#LON=np.asarray(LON, dtype=np.float32)

#print(LAT)
#print(type(lats))
#print(type(LAT))

#print(grb.latlons())
 

#print(closestlat,closestlon)
#print(LAT)
#for state in states:
##
#    print(state)
file.close()
