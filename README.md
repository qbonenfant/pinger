# pinger
Simple connectivity checker and logger

Just run it as  "python3 pinger.py" and redirect the stderr output to a file (or /dev/null).
It will create a log file in the same folder with a timestamp, and log any disconnection event lasting more than 10 seconds.
The stderr output will just tell you the status at a given time of the day (either OK or Disconnected).
