import sys, os
sys.path.append("c:/users/" + os.getlogin() + "/scoop/apps/python/current/lib/site-packages/dataextract")

try:
  import datetime
  import random
  import time
  import hashlib
  import string
  from threading import Thread
  from colorama import Fore, Style
except ImportError:
  print("Error: Missing module(s) please install the following module(s): colorama, datetime and hashlib.")


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
def bruteforce(target, print=None):
  staticList = []
  targetList = []
  initTime = time.time()
  for character in target:
    targetList.append(character)
    staticList.append(character)
  for i in range(60, 100):
    random.shuffle(targetList)

  while targetList != staticList:
    random.shuffle(targetList)
    if targetList == target:
      break

  endTime = time.time()
  elapsedtime = endTime - initTime

  if print != None:
    print(''.join(targetList))
    print("Bruteforce took:", elapsedtime, "seconds")
  else:
    return elapsedtime
  

def generate(length, type=None):
  if type == str("binary"):
    returniteam = []
    for i in range(length):
      temp = str(random.randint(0, 1))
      returniteam.append(temp)
      
  if type == str("password"):
    returniteam = []
    dataset = string.ascii_letters + string.digits
    for i in range(length):
      returniteam.append(random.choice(dataset))
      
  if type == str("address"):
    returniteam = []
    dataset = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
      returniteam.append(random.choice(dataset))
      
  if type == str("number"):
    returniteam = []
    dataset = string.digits + string.digits
    for i in range(length):
      returniteam.append(random.choice(dataset))

  return ''.join(returniteam)

