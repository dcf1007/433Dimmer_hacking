#!/usr/bin/env python

import time
import pigpio
import argparse
import statistics
import csv

parser = argparse.ArgumentParser(description='Monitor GPIO activity and print it or save it to a file.')
parser.add_argument('GPIOs', metavar='N', type=int, nargs='*', help='GPIO pins to monitor, separated by spaces')
parser.add_argument('file_in', help='File containing the data')

args = parser.parse_args()

data = {}

with open(args.file_in, newline='') as csvfile:
   csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   # Data has the following structure:
   #             ; Remote 1; Remote 2; Remote N; ...
   # Command name; 24-bit  ; 24-bit  ; 24-bit  ; ...

   # Store the remote names (header)
   remote_names = next(csv_reader)[1:]
   print(remote_names)
   # Loop through the rows of data
   for row in csv_reader:
      print(row)
      command_name = row.pop(0).strip()
      print(row)
      for i, col in enumerate(row):
         data.setdefault(row[i].strip()[0:16], {})["name"] = remote_names[i].strip()
         data[row[i].strip()[0:16]][row[i].strip()[16:]] = command_name.strip()

# Define the variables needed
pi = pigpio.pi()
signal_data = {}
data_capture = {}
tick_last = {}
cb = {}

# Check that pigpiod is running
if not pi.connected:
   exit()

# The option for all pins is disabled since the function for naming the signals was added
# Re-enabling it would be easy but it is not necessary for my case-scenario.
if len(args.GPIOs) == 0:
   G = range(0, 32)
else:
   G = args.GPIOs

# Initialize the variables for all the GPIO pins
device_number = 0
for g in G:
   pi.set_glitch_filter(g, 250)
   tick_last[g] = None
   signal_data[g] = [[],]
   data_capture[g] = False

# Define the callback function
def cbf(GPIO, level, tick):
   # Check wether is the first edge detected
   if tick_last[GPIO] == None:
      tick_last[GPIO] = tick

   # If it's not the first edge and we have something to measure against
   else:
      # Calculate the delta for the starting time and the pulse length
      dtick_last = pigpio.tickDiff(tick_last[GPIO], tick)
      
      # Check if it was a prelude pulse (12ms and low level)
      # The interrupt detects edge changes, so if level is 1 means it has been at 0 until now
      if (dtick_last > 11000) and (13000 > dtick_last) and (level == 1):
         if data_capture[GPIO] == True:
            #print("Preample. Repeat of data")

            # Check wether the previously received data packet is intact
            if len(signal_data[GPIO][-1]) != 24:
               print("Integrity check for last data package failed")

               # Delete the contents of the last repeat
               signal_data[GPIO][-1] = []
            else:
               codeword = str.join("", [str(statistics.mode(x)) for x in zip(*signal_data[GPIO])])
               #print(codeword)
               print(data[codeword[0:16]]["name"], data[codeword[0:16]][codeword[16:]])
               # Create a new entry in the list to append the new repeat
               signal_data[GPIO].append([])
         else:
            #print("Preamble. Init data capture")

            # Signal that valid data is being captured
            data_capture[GPIO] = True

            # Empty any signals that were stored
            signal_data[GPIO] = [[],]
      
      elif (dtick_last > 1000) and (data_capture[GPIO] == True):
         #print("Data bit received")

         # Store the data bit in the dictionary
         signal_data[GPIO][-1].append(1 - level)

      elif ((dtick_last > 13000) or (350 > dtick_last)) and (data_capture[GPIO] == True):
         #print("Not data anymore")
         signal_data[GPIO].pop()
         if len(signal_data[GPIO]) > 0:
            codeword = str.join("", [str(statistics.mode(x)) for x in zip(*signal_data[GPIO])])
            #print(codeword)
            print(data[codeword[0:16]]["name"], data[codeword[0:16]][codeword[16:]])
         data_capture[GPIO] = False
      
      tick_last[GPIO] = tick

# Add a callback for each defined GPIO pin
for g in G:
   cb[g] = pi.callback(g, pigpio.EITHER_EDGE, cbf)

# Wait for the callbacks to finish capturing data
try:
   while True:
      time.sleep(1)
except (KeyboardInterrupt, TimeoutError) as e:
   print(e)
   print("Tidying up")

   for c in cb.values():
      c.cancel()
   pi.stop()
