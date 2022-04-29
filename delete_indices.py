#!/usr/bin/env python3

# Testing commands
# ./mklogs && TOTAL_LOGS=$(ls -l logs|wc -l) && ./delete_indices.py && echo "Total logs before: ${TOTAL_LOGS}" && echo "Total logs after: $(ls -l logs|wc -l)" 
#

from os import listdir, remove
import re, datetime

LOGDIR="logs" # path to log file directory relative to this script
indices_age_days=10 # delete log files older than N days old - +/- 24 hours


for FILE in listdir(LOGDIR):
    #get the y,m,d from the file name
    [y,m,d] = re.split('[\.]', re.split('[\-]', FILE)[2] )[0:3]
    # Format for datetime
    ttime = datetime.datetime(int(y),int(m),int(d),0,0,0)
    # Get the seconds from then to now
    total_secs = int( (datetime.datetime.utcnow()- ttime).total_seconds() )

    if (total_secs > ( (indices_age_days)*86400)):
        DELETE_LOG=LOGDIR+"/"+FILE
        print("Removing:", DELETE_LOG)
        remove(DELETE_LOG)
