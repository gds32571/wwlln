#!/bin/bash

# change two values below to export a runevent
# http://www.sqlitetutorial.net/sqlite-tutorial/sqlite-export-csv/

sqlite3 ./lightning-strike.db <<"EOF" 
.headers on 
.mode csv 
.output map2.csv 
select * from events where runevent >= 88;
.quit
EOF
