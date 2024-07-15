#!/usr/bin/env python

# monitor.py
# 2016-09-17
# Public Domain

# monitor.py          # monitor all GPIO
# monitor.py 23 24 25 # monitor GPIO 23, 24, and 25

import sys
import time
import pigpio

#capture_finished = [False]*32
capture_finished = False
first = [None]*32
last = [None]*32
cb = []

capture_time = 1e6 #In micro-seconds

def cbf(GPIO, level, tick):
   global capture_finished

   if first[GPIO] == None:
      first[GPIO] = tick
   elif pigpio.tickDiff(first[GPIO], tick) < capture_time:
      if last[GPIO] != None:
         # When rising it changes from 0 to 1
         if level == 1:
            print(pigpio.tickDiff(first[GPIO], tick), GPIO, 0, pigpio.tickDiff(last[GPIO], tick))
            print(pigpio.tickDiff(first[GPIO], tick), GPIO, 1, "")
         # When falling it changes from 1 to 0
         else:
            print(pigpio.tickDiff(first[GPIO], tick), GPIO, 1, pigpio.tickDiff(last[GPIO], tick))
            print(pigpio.tickDiff(first[GPIO], tick), GPIO, 0, "")
      last[GPIO] = tick
   else:
      #capture_finished[GPIO] = True
      capture_finished = True

pi = pigpio.pi()

if not pi.connected:
   exit()

if len(sys.argv) == 1:
   G = range(0, 32)
else:
   G = []
   for a in sys.argv[1:]:
      G.append(int(a))

for g in G:
   cb.append(pi.callback(g, pigpio.EITHER_EDGE, cbf))

try:
   #while any(capture_finished) == False:
   while capture_finished == False:
      time.sleep(0.1)
except KeyboardInterrupt:
   print("\nTidying up")
   for c in cb:
      c.cancel()

pi.stop()
