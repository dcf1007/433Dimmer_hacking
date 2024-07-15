#!/usr/bin/env python

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
            print(GPIO, pigpio.tickDiff(first[GPIO], tick), 0, pigpio.tickDiff(last[GPIO], tick))
            print(GPIO, pigpio.tickDiff(first[GPIO], tick), 1, "")
         # When falling it changes from 1 to 0
         else:
            print(GPIO, pigpio.tickDiff(first[GPIO], tick), 1, pigpio.tickDiff(last[GPIO], tick))
            print(GPIO, pigpio.tickDiff(first[GPIO], tick), 0, "")
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
