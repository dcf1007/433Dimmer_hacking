#!/usr/bin/env python

# monitor.py
# 2016-09-17
# Public Domain

# monitor.py          # monitor all GPIO
# monitor.py 23 24 25 # monitor GPIO 23, 24, and 25

import time
import pigpio
import argparse

parser = argparse.ArgumentParser(description='Monitor GPIO activity and print it or save it to a file.')
parser.add_argument('GPIOs', metavar='N', type=int, nargs='*', help='GPIO pins to monitor, separated by spaces')

args = parser.parse_args()

pi = pigpio.pi()
timeout = 30 #Timeout in second
capture_finished = {}
first = {}
last = {}
cb = {}

if not pi.connected:
   exit()

if len(args["GPIOs"]) == 0:
   G = range(0, 32)
else:
   G = args["GPIOs"]

for g in G:
   capture_finished[g] = False
   first[g] = None
   last[g] = None

capture_time = 1e6 #In micro-seconds

def cbf(GPIO, level, tick):
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
      capture_finished[GPIO] = True

print("GPIO", "Time(μs)", "Level", "Duration(μs)")

for g in G:
   cb[g] = pi.callback(g, pigpio.EITHER_EDGE, cbf)

try:
   start_time = time.time()
   while all(capture_finished.values()) == False:
      if time.time() - start_time > timeout:
         print("time out")
         break
      time.sleep(1)
except KeyboardInterrupt:
   print("\nTidying up")
   for c in cb.values():
      c.cancel()

pi.stop()