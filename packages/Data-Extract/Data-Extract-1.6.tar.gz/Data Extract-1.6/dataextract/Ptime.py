# This is a module for time this will also be implemented in standalone
try:
  import datetime
  import time
  import string
  import os
except ImportError:
  print("Error: Missing module(s) please install the following module(s): random, time, hashlib, string")


# Global variables
class errorMessages():
  error = str("ERROR: An unknown error has occured.")
  fileUnreadable = str("ERROR: The file given cannot be read.")
  fileEmpty = str("ERROR: The given file is empty and contains no data.")
  insufficientPerm = str("ERROR: The file cannot be accessed due to insufficient permissions.")
  fileExists = str("ERROR: The file does not exist/the path can't be found.")
  fileOpen = str("ERROR: The file cannot be opened due to it being in use by another process.")   

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
time = datetime.datetime.now().strftime("%H:%M:%S") + "\n\n"
date = datetime.datetime.now().strftime("%Y-%m-%d") + "\n\n"


# Functions
def nowtime(time=None, date=None):
  if time is False or date is True:
    return date
  if time is True or date is False:
    return time
  else:
    return now
  

def currentdate():
  return date


def currenttime():
  return time