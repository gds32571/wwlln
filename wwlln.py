#!/usr/bin/env python3

# Originally a test program from Aaron Bach, creator of the 
# aiowwlln python3 library
# see https://github.com/bachya/aiowwlln
#
# this version by Gerald Swann
# version 1.1
# added csv file export so that the strikes can be put on a google map.


import asyncio
from datetime import timedelta
import datetime
from time import gmtime

from aiohttp import ClientSession

from aiowwlln import Client
from aiowwlln.errors import WWLLNError

import json
import csv

TARGET_LATITUDE = 30
TARGET_LONGITUDE = -90
TARGET_RADIUS_MILES = 225
TARGET_TIME_MINUTES = 45

# these flags do things
debug = 0
myCSV = 1

data = []
b = {}
b2 = {}

async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        try:
            # Create a client:
            client = Client(websession)

            # Get all strike data:
#            print(await client.dump())

            # Get strike data within a specified radius around a set of coordinates _and_
            # within the target time:
            strike_data = await client.within_radius(
                    TARGET_LATITUDE,
                    TARGET_LONGITUDE,
                    TARGET_RADIUS_MILES,
                    unit="imperial",
                    window=timedelta(minutes=TARGET_TIME_MINUTES),
                )

            if len(strike_data) == 0:
               print("No data for this location, radius and time window.")
            
            if (len(strike_data) > 0):

                strike_data = str(strike_data)
                strike_data = strike_data.replace("\'", "\"")

                decoded = json.loads(strike_data)    
                
                if myCSV == 1:

                   export_data = open('./wwlln_lightning.csv', 'w')
                   # create the csv writer object
                   csvwriter = csv.writer(export_data)

                   count = 0
                   for strike in decoded:
                     if count == 0:
                         header = (["key", "Latitude", "Longitude", "Distance", "Date"])
                         csvwriter.writerow(header)
                         count += 1

                     myKey = strike

                     xtime = int(decoded[strike]["unixTime"])
                     myDate = datetime.datetime.fromtimestamp(xtime)

                     myLat = decoded[strike]["lat"]
                     myLong = decoded[strike]["long"]
                     myDist = round(decoded[strike]["distance"],2)

                     csvwriter.writerow( [myKey,myLat,myLong,myDist,myDate ] )
                   export_data.close()

                for key in decoded: 
                    if debug == 1:
                       print(key)
                       print(decoded[key]["distance"])
                    b[key]= decoded[key]["distance"]
                    b2[key]= decoded[key]["unixTime"]

                c = sorted(b.items(), key=lambda x: x[1]) 
                c2 = sorted(b2.items(), key=lambda x: x[1],reverse=True) 
                key_closest = c[0][0]   
                key_recent = c2[0][0]   

                if debug == 1:
                  print("Sorted by distance\n")
                  for x in range(len(c)):
                      print("key = ",c[x][0]," ","distance = ",decoded[c[x][0]]["distance"])
                      print(decoded[c[x][0]])
                      print("\n")

                print("\n")      
                print("Radius (miles)= ",TARGET_RADIUS_MILES)
                print("Window (minutes)= ", TARGET_TIME_MINUTES)

                print("Number of records= ",end='')    
                print(len(decoded))
                print("\n")

                print("Closest strike key= ",key_closest)   
                x = key_closest 
                print("key = ",x," ","distance = ",decoded[x]["distance"])
                print(decoded[x])
                print('{}-{:>02}-{:>02} {:>02}:{:>02}:{:>02}'.format(*gmtime(decoded[x]["unixTime"])))

                diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(decoded[x]["unixTime"])
                print("h:m:s ago = ",diff)
                minutes = round(diff.seconds/60,1)
                print("minutes ago= ",minutes)
                print("\n")

                print("most recent strike key= ",key_recent)   
                x = key_recent
                print("key = ",x," ","distance = ",decoded[x]["distance"])
                print(decoded[x])
                print('{}-{:>02}-{:>02} {:>02}:{:>02}:{:>02}'.format(*gmtime(decoded[x]["unixTime"])))

                diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(decoded[x]["unixTime"])
                print("h:m:s ago = ",diff)
                minutes = round(diff.seconds/60,1)
                print("minutes ago= ",minutes)

                print("\n")



        except WWLLNError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
