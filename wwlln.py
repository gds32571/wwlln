#!/usr/bin/env python3

#*****************************

#wwlln.py
#written 22 July 2019 - gswann

#*****************************


# """Run an example script to quickly test."""
import asyncio
from datetime import timedelta
import datetime
from time import gmtime

from aiohttp import ClientSession

from aiowwlln import Client
from aiowwlln.errors import WWLLNError

import json

TARGET_LATITUDE = 24.84
TARGET_LONGITUDE = 1.71
TARGET_RADIUS_MILES = 50
TARGET_TIME_MINUTES = 60

debug = 0

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

            # Get strike data within a 50km radius around a set of coordinates _and_
            # within the last hour:
            data = await client.within_radius(
                    TARGET_LATITUDE,
                    TARGET_LONGITUDE,
                    TARGET_RADIUS_MILES,
                    unit="imperial",
                    window=timedelta(minutes=TARGET_TIME_MINUTES),
                )

#            print(len(data),data)

            if (len(data) > 0):
                data = str(data)
                data = data.replace("\'", "\"")

                decoded = json.loads(str(data))    

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
