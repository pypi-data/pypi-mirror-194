import sys, os
sys.path.append("c:/users/" + os.getlogin() + "/scoop/apps/python/current/lib/site-packages/dataextract")

import string

def tick(inc, args=None):
  tickVar = 0
  argB = "set"
  argC = "reset"
  
  if args == argB:
    tickVar += inc
    print(tickVar)
  if args == argC:
    tickVar = 0
    print(tickVar)
  else:
    tickVar += inc
    
  return tickVar

