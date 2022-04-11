# coding=utf-8
#
#############################################
#
#  Pinger - Simple connection logger
#
#
#

import sys
import os
from time import sleep
from datetime import datetime, timedelta
from random import shuffle

# Constants
check_delay = 10  # time between checks, 10 sec by default
dc_delay = 5  # changing delay if we are deconnected, check evey 5 seconds.
# Formats
time_format = "%H:%M:%S"
full_format = "%d_%m_%Y_%H:%M:%S"
date_format = "%d %B %Y"


# List of hostnames, feel free to change them as you want.
# I just put some i think should "always" be up.
hostnames = ["google.com", "reddit.com", "amazon.fr", "youtube.fr"]


def check_connection():
    """Check the connectivity status by pinging "always up" servers.
    Return True if we are connected to the internet."""

    global hostnames  # yeah,  i know...

    # Shuffling so we don't ping them at constant intervals.
    shuffle(hostnames)
    response = 1
    i = 0
    # check hosts until we run out or get a positive answer
    while(response != 0 and i < len(hostnames)):
        response = os.system("ping -c 1 " + hostnames[i] + " > /dev/null 2>&1")
        i += 1
    # if we get a response, status should be 0.
    return(response == 0)


def format_timedelta(delta):
    """Convert time delta in H:M:S string format."""

    # Extracting total amount of time from the time delta object
    total_s = delta.seconds
    # Computing individual amounts to hour resolution.
    s = total_s % 60
    total_s //= 60
    m = total_s % 60
    total_s //= 60
    h = total_s

    # Formatting
    H, M, S = "", "", ""
    if(h > 0):
        H = f"{str(h)} hour{'' if h==1 else 's'}, "
    if(m > 0):
        H = f"{str(m)} minute{'' if m==1 else 's'}, "
    S = f"{str(s)} second{'' if s==1 else 's'}."
    return(H + M + S)


def log(msg, file):
    """Store message in a log file."""
    logfile = open(file, "at")
    logfile.write(msg + "\n")
    logfile.close()


def print_err(msg, now_time):
    """Just print to stderr with a time stamp"""
    timestamp = now_time.strftime(time_format)
    print(timestamp + "\t" + msg, file=sys.stderr, flush=True)


def main():
    """Log disconnection events."""

    cut = False  # Connection was recently lost
    wait = check_delay  # Adjusting the loop frequency according to events

    # remember when was the last time we were connected
    last_connection = datetime.now()

    # Init the log file
    #   Creation time
    start_time = datetime.now()
    #   Log file name
    logfn = f"log_{start_time.strftime(full_format)}.txt"
    #   Writting first entry
    logfile = open(logfn, "w")
    logfile.write(f"Logging started at {start_time.strftime(time_format)} ")
    logfile.write(f"on {start_time.strftime(date_format)}.\n")
    logfile.close()

    # main loop
    while(True):

        # Vibe check and time tracking
        status = check_connection()
        current_time = datetime.now()
        # Everything is Ok
        if(status):
            # If connection was previously lost, update log
            if(cut):
                cut = False
                delta = format_timedelta(current_time - last_connection)
                log(f"Recovered, disconnection lasted {delta}\n", logfn)
                wait = check_delay
            # stderr display
            print_err("OK", current_time)

            last_connection = current_time

        # Everything is RUINED!
        else:
            print_err("Disconnected", current_time)
            # Log disconnection start
            if(not cut):
                cut = True       # We are now disconnected
                msg = f"Disconnected at {current_time.strftime(time_format)} "
                msg += f"on {current_time.strftime(date_format)}."
                log(msg, logfn)
                wait = dc_delay  # increase check frequency
        sleep(wait)



if(__name__ == "__main__"):
    main()
