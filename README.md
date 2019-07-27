# wwlln
Test program for the WWLLN website with Aaron Bach's aiowwlln library.

Uses python3 to access the wwlln website data, filtering by radius and time window.  The program captures data within the range, than prints out the most recent strike, and the closest.

The csv flag lets you export data into csv format file.
Includes example csv file that can be imported on Google maps.

Added code to save data intoa SQLite database for subsequent query.

### createtable.py 
   Creates the SQL database tables required by the program
   
### export_to_csv.sh   
   An editable file to export data from SQL into a CSV file for Google maps.
   
   
Worth playing with if you are trying out the Home Assistant component.

