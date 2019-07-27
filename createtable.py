#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('./lightning-strike.db')
c = conn.cursor()

c.execute('''drop table events''')
c.execute('''drop table runevents''')
conn.commit()


# Create table
c.execute('''CREATE TABLE events
             (runevent int, eventid int PRIMARY KEY, datetime text, lat real, long real, distance real)''')
c.execute('''CREATE TABLE runevents
             (runevent int PRIMARY KEY, datetime text, target_lat real, target_long real, target_radius int,  nodup int, dup int )''')

# Insert a row of data
# c.execute("INSERT INTO runevents VALUES (1,'2019-07-26 07:00:00')")

# Save (commit) the changes
conn.commit()
conn.close()
