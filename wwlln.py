#!/usr/bin/env python3

# Originally a test program from Aaron Bach, creator of the 
# aiowwlln python3 library
# see https://github.com/bachya/aiowwlln
#
# this version by Gerald Swann
# version 1.1
# added csv file export so that the strikes can be put on a google map.

import pdb

import asyncio
from datetime import timedelta
import datetime
from time import gmtime

from aiohttp import ClientSession

# pdb.set_trace()

from aiowwlln import Client
from aiowwlln.errors import WWLLNError

import json
import csv

import sqlite3

TARGET_LATITUDE = 28.840809
TARGET_LONGITUDE = -82.002535
TARGET_RADIUS_MILES = 100
TARGET_TIME_MINUTES = 120

# these flags do things
# print extra info
debug = 0
# save data in CSV format file for Google maps
myCSV = 1
# insert data into sql database for analysis
# can't do SQL unless also doing CSV
mySQL = 1

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
               print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),end = '  ') 

               print("No data for this location, radius and time window.")
            
            if (len(strike_data) > 0):

                print("********************************")
                dup = 0
                strike_data = str(strike_data)
                strike_data = strike_data.replace("\'", "\"")

                decoded = json.loads(strike_data)    
                
                if myCSV == 1:

                   export_data = open('./wwlln_lightning.csv', 'w')
                   # create the csv writer object
                   csvwriter = csv.writer(export_data)

                   count = 0
                   dup = 0
                   nodup = 0
                   
#                   pdb.set_trace()
                   if mySQL == 1:    
                     conn = sqlite3.connect('./lightning-strike.db')

                     cur = conn.cursor()
                     cur.execute('select max(runevent) from runevents')
                     row = (cur.fetchone())
                     cur.close

                     if row[0] is None:
                        eventnumber = 1
                     else:
                        eventnumber = int(row[0]) + 1

                     print("Recording event number: ",end='')
                     print (eventnumber)
                     cur.close

                     curtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                     print(curtime)
                     
                   for strike in decoded:
                     if count == 0:
                         header = (["EventID", "Datetime", "Latitude", "Longitude", "Distance"])
                         csvwriter.writerow(header)
                         count += 1

                     myEventID = strike

#                     pdb.set_trace()
                     unixtime = int(decoded[strike]["unixTime"])
                     myDate = datetime.datetime.fromtimestamp(unixtime)

                     myDate = myDate.strftime("%Y-%m-%d %H:%M:%S")


                     myLat = decoded[strike]["lat"]
                     myLong = decoded[strike]["long"]
                     myDist = round(decoded[strike]["distance"],2)

                     csvwriter.writerow( [myEventID, myDate, myLat,myLong,myDist ] )

#                     pdb.set_trace()
                     if mySQL == 1:    
                        myData = [(eventnumber,myEventID,myDate,myLat,myLong,myDist)]

                        cur = conn.cursor()
                        cur.execute('select count(*) from events where eventid = (?)', [myEventID])
                        rowcount = cur.fetchone()[0]
                        if rowcount > 0:
                           dup = dup + 1
                        else:
                           nodup = nodup + 1   
                        cur.close()
                        cur = conn.cursor()
                        cur.executemany('INSERT OR IGNORE INTO events VALUES (?,?,?,?,?,?)', myData)
#                        conn.commit()

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
                if mySQL == 1:
                   print ("Inserted " + str(nodup) + " rows, ignored " + str(dup) + " rows")
                print("\n")

                print("Closest strike key= ",key_closest)   
                x = key_closest 
                print("key = ",x," ","distance = ",round(decoded[x]["distance"],2))
                print(decoded[x])
                print('{}-{:>02}-{:>02} {:>02}:{:>02}:{:>02}'.format(*gmtime(decoded[x]["unixTime"])))

                diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(decoded[x]["unixTime"])
                print("h:m:s ago = ",diff)
                minutes = round(diff.seconds/60,1)
                print("minutes ago= ",minutes)
                print("\n")

                print("most recent strike key= ",key_recent)   
                x = key_recent
                print("key = ",x," ","distance = ",round(decoded[x]["distance"],2))
                print(decoded[x])
                print('{}-{:>02}-{:>02} {:>02}:{:>02}:{:>02}'.format(*gmtime(decoded[x]["unixTime"])))

                diff = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(decoded[x]["unixTime"])
                print("h:m:s ago = ",diff)
                minutes = round(diff.seconds/60,1)
                print("minutes ago= ",minutes)

                print("\n")

                if mySQL == 1:
                     cur = conn.cursor()
                     cur.executemany('INSERT INTO runevents VALUES (?,?,?,?,?,?,?)',\
                      [(eventnumber,curtime, TARGET_LATITUDE, TARGET_LONGITUDE, TARGET_RADIUS_MILES, nodup, dup)])
                     cur.close
                     # this commit should be for runevens and events as well.
                     # an atomic unit so to speak.
                     conn.commit()
                     conn.close()

        except WWLLNError as err:
            print(err)


asyncio.get_event_loop().run_until_complete(main())
