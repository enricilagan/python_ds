"""Extract datetime from log entries and calculate the time
   between the first and last shutdown events"""
from datetime import datetime
import os
import urllib.request

SHUTDOWN_EVENT = 'Shutdown initiated'

# prep: read in the logfile
logfile = os.path.join('/tmp', 'log')
urllib.request.urlretrieve('http://bit.ly/2AKSIbf', logfile)

with open(logfile) as f:
    loglines = f.readlines()


# for you to code:

def convert_to_datetime(line):
    """Given a log line extract its timestamp and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)"""
    lines = line.split(" ")
    date_info = lines[1]
    return datetime(int(date_info[0:4]), int(date_info[5:7]),
                    int(date_info[8:10]), int(date_info[11:13]),
                    int(date_info[14:16]), int(date_info[17:19]))


def time_between_shutdowns(log):
    """Extract shutdown events ("Shutdown initiated") from loglines and calculate the
       timedelta between the first and last one.
       Return this datetime.timedelta object."""
    log_event = []
    for line in log:
        if SHUTDOWN_EVENT in line:
            time_stamp = convert_to_datetime(line)
            log_event.append(time_stamp)
    return log_event[-1] - log_event[0]
