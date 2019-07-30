#!/bin/bash

# change two values below to export a runevent
# http://www.sqlitetutorial.net/sqlite-tutorial/sqlite-export-csv/

sqlite3 ./lightning-strike.db <<"EOF" 
.headers on 
.mode csv 
.output map0730.csv 
select * from events where distance < 50 and datetime > '2019-07-29 20:00:00';
.quit
EOF

#select * from events where runevent >= 156;
