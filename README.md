# wwlln project

### wwlln.py
Test program for the WWLLN website with Aaron Bach's aiowwlln library.

Uses python3 to access the wwlln website data, filtering by radius and time window.  The program captures data within the range, than prints out the most recent strike, and the closest.

The csv flag lets you export data into csv format file.
Includes example csv file that can be imported on Google maps.

Added code to save data into a SQLite database for subsequent query.  The program checks for existing event ids, skips those, 
and inserts the rest of the records.  These are the variables dup and nodup.  There is a runevent that uniquely identifies a specific program run.

### Program output:
<pre>
********************************
Recording event number: 252
2019-07-30 05:00:04

Radius (miles)=  100
Window (minutes)=  120
Number of records= 15
Inserted 6 rows, ignored 9 rows

Closest strike key=  9603765
key =  9603765   distance =  83.18
{'unixTime': 1564474913.5, 'lat': 28.49, 'long': -80.69, 'distance': 83.18248834860982}
2019-07-30 08:21:53
h:m:s ago =  0:38:11.483379
minutes ago=  38.2

most recent strike key=  8896633
key =  8896633   distance =  84.53
{'unixTime': 1564475318.3, 'lat': 28.51, 'long': -80.66, 'distance': 84.5324585791536}
2019-07-30 08:28:38
h:m:s ago =  0:31:26.683549
minutes ago=  31.4
</pre>

### result.txt
I run the program from cron and output the run print data into result.txt.  You can tail this file to see what is happening. Here is the crontab entry:

*/5 * * * * cd ./wwlln ; /usr/local/bin/python3 ./wwlln.py >> result.txt 2>&1


### createtable.py 
   Creates the SQL database tables required by the program
   
### export_to_csv.sh   
   An editable file to export data from SQL into a CSV file for Google maps.  Put any SQL query to map the data 
you are interested in.  You should identify a filename for output in the SQL code portion of this shell script.
   
   
Worth playing with if you are trying out the Home Assistant component.

### Data set testing 
I spent some time 29 July 2019 downloading datasets from the WWLLN website and comparing consective 
downloads.  I discovered several things:

Each data set contains 5001 lightning strike records.
At whatever instant you request the data, the web site subtracts 30 minutes as the most
recent data you are allowed to have. Then it adds 5001 records to the end of that. So the 
timestamp on the most recent record will be now() - 30 minutes.  The oldest time stamp will 
vary depending on world wide lightning activitiy.  Last night, that value was about 10 - 13 minutes or so.

So if you request data less often that every 5-8 minutes, you will probably miss records.

Here is how I understand the <b>window</b> that is part of Aaron's library: if lightning activity on ythe whole planet is very slight, then you could get much older data in the 5001 records that are downloaded.  That is when the window would be helpful to limit that data returned from <b>client.within_radius</b>. Otherwise, at less than 10 minutes age from first to last record, it would not really matter.



