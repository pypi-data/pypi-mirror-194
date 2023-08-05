import sys, os
sys.path.append("c:/users/" + os.getlogin() + "/scoop/apps/python/current/lib/site-packages/dataextract")

# Imports
import os
import sys
from sys import platform


# Global variables
class colorCodes():
  black = int(0);
  blue = int(1);
  green = int(2);
  aqua = int(3);
  red = int(4);
  purple = int(5);
  yellow = int(6);
  white = int(7);
  grey = int(8);
  light_blue = int(9);
  light_green = str('A');
  light_aqua = str('B');
  light_red = str('C');
  light_purple = str('D');
  light_yellow = str('E');
  bright_white = str('F');

def ResetAll():
  os.system("Color " + colorCodes.black + colorCodes.white)
def clear():
  if platform == "linux" or platform == "linux2":
    os.system("clear")
  else:
    os.system("cls")


class text():
  def Black():
    os.system("Color " + str(colorCodes.black))
  def Blue():
    os.system("Color " + str(colorCodes.blue))
  def Green():
    os.system("Color " + str(colorCodes.green))
  def Aqua():
    os.system("Color " + str(colorCodes.aqua))
  def Red():
    os.system("Color " + str(colorCodes.red))
  def Purple():
    os.system("Color " + str(colorCodes.purple))
  def Yellow():
    os.system("Color " + str(colorCodes.yellow))
  def White():
    os.system("Color " + str(colorCodes.white))
  def Grey():
    os.system("Color " + str(colorCodes.grey))
  def Lightblue():
    os.system("Color " + str(colorCodes.light_blue))
  def Lightgreen():
    os.system("Color " + str(colorCodes.light_green))
  def Lightaqua():
    os.system("Color " + str(colorCodes.light_aqua))
  def Lightred():
    os.system("Color " + str(colorCodes.light_red))
  def Lightpurple():
    os.system("Color " + str(colorCodes.light_purple))
  def Lightyellow():
    os.system("Color " + str(colorCodes.light_yellow))
  def Brightwhite():
    os.system("Color " + str(colorCodes.light_white))
  
  def Reset():
    os.system("Color " + int(colorCodes.black))
  def clear():
    if platform == "linux" or platform == "linux2":
      os.system("clear")
    else:
      os.system("cls")
  
  
class background():
  def Black():
    os.system("Color " + str(colorCodes.black + colorCodes.white))
  def Blue():
    os.system("Color " + str(colorCodes.blue + colorCodes.white))
  def Green():
    os.system("Color " + str(colorCodes.green + colorCodes.white))
  def Auqa():
    os.system("Color " + str(colorCodes.aqua + colorCodes.white))
  def Red():
    os.system("Color " + str(colorCodes.red + colorCodes.white))
  def Purple():
    os.system("Color " + str(colorCodes.purple + colorCodes.white))
  def Yellow():
    os.system("Color " + str(colorCodes.yellow + colorCodes.white))
  def White():
    os.system("Color " + str(colorCodes.white + colorCodes.black))
  def Grey():
    os.system("Color " + str(colorCodes.grey + colorCodes.black))
  def Lightblue():
    os.system("Color " + str(colorCodes.light_blue + colorCodes.white))
  def Lightgreen():
    os.system("Color " + str(colorCodes.light_green + colorCodes.white))
  def Lightaqua():
    os.system("Color " + str(colorCodes.light_aqua + colorCodes.white))
  def Lightred():
    os.system("Color " + str(colorCodes.light_red + colorCodes.white))
  def Lightpurple():
    os.system("Color " + str(colorCodes.light_purple + colorCodes.white))
  def Lightyellow():
    os.system("Color " + str(colorCodes.light_yellow + colorCodes.white))
  def Brightwhite():
    os.system("Color " + str(colorCodes.light_white + colorCodes.white))
  
  def Reset():
    os.system("Color " + str(colorCodes.black))
  def clear():
    if platform == "linux" or platform == "linux2":
      os.system("clear")
    else:
      os.system("cls")


class style():
  def Bright():
    os.system("Color " + str(colorCodes.bright_white))
  def Dim():
    os.system("Color " + str(colorCodes.grey))
  def ResetAll():
    os.system("Color " + str(colorCodes.black + colorCodes.white))
    

