# This is a module for easy logging in python this will also be implemented in standalone
try:
  import datetime
  import time
  import os
  from colorama import Fore, Style
except ImportError:
  print("Error: Missing module(s) please install the following module(s): colorama, datetime and os.")


# Global variables
class errorMessages():
  error = str("ERROR: An unknown error has occured.")
  fileUnreadable = str("ERROR: The file given cannot be read.")
  fileEmpty = str("ERROR: The given file is empty and contains no data.")
  insufficientPerm = str("ERROR: The file cannot be accessed due to insufficient permissions.")
  fileExists = str("ERROR: The file does not exist/the path can't be found.")
  fileOpen = str("ERROR: The file cannot be opened due to it being in use by another process.")   

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"


# Functions
def eventlog(message, file):
  if os.path.exists(file):
    with open(file, "w") as fin:
      fin.write(message + " - AT: " + now)
      fin.close()
  else:
    print(errorMessages.fileExists)
    raise FileNotFoundError
  
  
def errorlog(message, file):
  if os.path.exists(file):
    with open(file, "w") as fin:
      fin.write("ERROR: " + message + " - AT: " + now)
      fin.close()
    print(Fore.RED + "ERROR: " + message + Style.RESET_ALL)
  else:
    print(errorMessages.fileExists)
    raise FileNotFoundError
  

def userlog(message):
  print(Fore.BLUE + "LOG: " + Fore.GREEN + message + Style.RESET_ALL)
  time.sleep(3)
  
  