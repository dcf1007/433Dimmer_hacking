#!/usr/bin/env python

# monitor.py
# 2016-09-17
# Public Domain

# monitor.py          # monitor all GPIO
# monitor.py 23 24 25 # monitor GPIO 23, 24, and 25

import time
import pigpio
import argparse
import csv

parser = argparse.ArgumentParser(description='Monitor GPIO activity and print it or save it to a file.')
parser.add_argument('GPIOs', metavar='N', type=int, nargs='*', help='GPIO pins to monitor, separated by spaces')
parser.add_argument('--name', help='Prefix to use when saving the data')

args = parser.parse_args()

pi = pigpio.pi()
timeout = 10 #Timeout in second
data = {}
plot = {}
capture_finished = {}
first = {}
last = {}
cb = {}

if not pi.connected:
   exit()

if len(args.GPIOs) == 0:
   G = range(0, 32)
else:
   G = args.GPIOs

for g in G:
   data[g] = []
   plot[g] = []
   capture_finished[g] = False
   first[g] = None
   last[g] = None

capture_time = 1e6 #In micro-seconds

def cbf(GPIO, level, tick):
   if first[GPIO] == None:
      first[GPIO] = tick
      # When rising it changes from 0 to 1
      if level == 1:
         plot[GPIO].append((GPIO, 0, 1, ""))
         print(GPIO, 0, 1, "")
      
      # When falling it changes from 1 to 0
      else:
         plot[GPIO].append((GPIO, 0, 0, ""))
         print(GPIO, 0, 0, "")
   
   elif pigpio.tickDiff(first[GPIO], tick) < capture_time:
      dFirst = pigpio.tickDiff(first[GPIO], tick)
      
      if last[GPIO] != None:
         dLast = pigpio.tickDiff(last[GPIO], tick)
         
         # When rising it changes from 0 to 1
         if level == 1:
            data[GPIO].append((GPIO, dFirst, level, dLast))
            plot[GPIO].append((GPIO, dFirst, 0, dLast))
            plot[GPIO].append((GPIO, dFirst, 1, ""))
            print(GPIO, dFirst, 0, dLast)
            print(GPIO, dFirst, 1, "")
         
         # When falling it changes from 1 to 0
         else:
            data[GPIO].append((GPIO, dFirst, level, dLast))
            plot[GPIO].append((GPIO, dFirst, 1, dLast))
            plot[GPIO].append((GPIO, dFirst, 0, ""))
            print(GPIO, dFirst, 1, dLast)
            print(GPIO, dFirst, 0, "")
         last[GPIO] = tick
      
      else:
         # When rising it changes from 0 to 1
         if level == 1:
            plot[GPIO].append((GPIO, dFirst, 1, ""))
            print(GPIO, dFirst, 1, "")
         
         # When falling it changes from 1 to 0
         else:
            plot[GPIO].append((GPIO, dFirst, 0, ""))
            print(GPIO, dFirst, 0, "")
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
         raise TimeoutError("Time out")
         break
      time.sleep(1)
   else:
      raise TimeoutError("Capturing done")
except (KeyboardInterrupt, TimeoutError) as e:
   print(e)
   print("Tidying up")

   for c in cb.values():
      c.cancel()
   pi.stop()

if args.name != None:
   print("Saving the collected data")

   with open(args.name + '_plot.csv', 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      csv_writer.writerow(["GPIO", "Time(μs)", "Level", "Duration(μs)"])
      for GPIO in plot:
         for plot_line in plot[GPIO]:
            csv_writer.writerow(plot_line)
   
   with open(args.name + '_raw.csv', 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      csv_writer.writerow(["GPIO", "Time(μs)", "Level", "Duration(μs)"])
      for GPIO in data:
         for data_line in data[GPIO]:
            csv_writer.writerow(data_line)