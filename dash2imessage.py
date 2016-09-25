#!/usr/bin/env python

import os
from scapy.all import *
import time

# The email address of someone in your contacts that you want to iMessage
email = "andy@andypowe11.net"
# MAC address of your Dash button - use finddash.py to obtain this
mac = "ac:63:be:d3:70:50"
# A filename in the current working directory, used to record the last time the button was pressed
fname = ".dash"

# Check datestamp on a file to see when the button was last pressed
def rememberpress():
  times=None
  with open(fname, 'a'):
    os.utime(fname, times)

# Touch the file to show that the button has just been pressed
def lastpressed():
  try:
    mtime = os.path.getmtime(fname)
  except OSError:
    mtime = 0
  return mtime

# Use AppleScript to send an iMessage
def sendimessage(msg):
  cmd = """osascript -e 'tell application "Messages"
                         send "%s" to buddy "%s" of (service 1 whose service type is iMessage)
                       end tell'""" % (msg, email)
  os.system(cmd)

# Called each time the Dash button wakes up and connects to the wifi network
def arp_monitor_callback(pkt):
  if ARP in pkt and pkt[ARP].op == 1: #who-has
    if pkt[ARP].hwsrc == mac:
      now = time.time()
      lt = time.localtime(now)
      # Time to get up
      if lt.tm_hour == 6 & lt.tm_min >= 58 & lt.tm_min <= 59:
        sendimessage("Rise and shine")
      elif lt.tm_hour == 7 & lt.tm_min >= 0 & lt.tm_min <= 9:
        sendimessage("Rise and shine")
      # Time for tea
      if lt.tm_hour == 18 & lt.tm_min >= 50 & lt.tm_min <= 59:
        sendimessage("Tea is ready")
      elif lt.tm_hour == 19 & lt.tm_min >= 0 & lt.tm_min <= 9:
        sendimessage("Tea is ready")
      # No response in 5 minutes... try again
      elif now - lastpressed() < 300:
        sendimessage("Now")
      # Do not disturb (work and/or sleep)
      # Send the default message (except during office or sleep hours)
      elif lt.tm_hour >= 16 & lt.tm_hour <= 23:
        sendimessage("Can you pop down please?")
      rememberpress()
      return pkt.sprintf("%ARP.hwsrc% Dash button pressed")

# Sit watching the network forever
sniff(prn=arp_monitor_callback, filter="arp", store=0)
