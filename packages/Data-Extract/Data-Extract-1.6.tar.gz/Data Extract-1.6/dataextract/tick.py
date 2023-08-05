import string
import os

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

