#!/usr/bin/env python

import time
import pigpio
import argparse
import csv

parser = argparse.ArgumentParser(description='Monitor GPIO activity and print it or save it to a file.')
parser.add_argument('GPIOs', metavar='N', type=int, nargs='+', help='GPIO pins to monitor, separated by spaces')
parser.add_argument('--prefix', help='Prefix to use when saving the data')
parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite the data if the file already exists')
parser.add_argument('-c', '--capture-time', type=float, default=1.0, help='Interval length to capture the signal')
parser.add_argument('-t', '--timeout', type=int, default=10, help='Time to wait if no signals are received')

args = parser.parse_args()

# Define the variables needed
pi = pigpio.pi()
device_names = {}
signal_names = {}
signal_data = {}
signal_plot = {}
capture_finished = {}
tick_first = {}
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

# If append was selected (default) load the devices and signals previously stored
stored_signals = {}
if not args.overwrite:
   try:
      # Attempt to open the file
      with open(args.prefix + '_raw.csv', newline='') as csvfile:
         csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
         # Data has the following structure:
         # GPIO; Device name; Signal name; Time (μs); Level; Duration (μs)

         # Skip the header
         next(csv_reader)

         # Loop through the rows of data
         for row in csv_reader:
            # Set the GPIO pin nr. as key and the rest of the columns as values
            stored_signals.setdefault(row[1], []).append(row[2])
   except FileNotFoundError:
      pass

# Initialize the variables for all the GPIO pins
device_number = 0
for g in G:
   if device_number != len(stored_signals):
      print("Previously stored devices:")
      for n, device_name in enumerate(stored_signals.keys()):
         print("  (" + str(n) + ")", device_name)
      device_number = len(stored_signals)
      print()
   
   # Assign names to the devices from each GPIO pin
   while True:
      if device_number != 0:
         print("Select a previously stored device or ", end='')
      device_name = input("Enter a new name for the device in GPIO " + str(g) + ": ")
      if device_name.isdigit():
         if len(stored_signals) > int(device_name):
            device_names[g] = list(stored_signals.keys())[int(device_name)]
            break
         else:
            continue
      else:
         device_names[g] = device_name
         stored_signals[device_name] = []
         break
   
   # Assign names to the signals to be captured for each GPIO pin
   while True:
      signal_name = input("Please name the signal for GPIO " + str(g) + ": ")
      if signal_name in stored_signals.get(device_names[g], []):
         print("A signal with this name has already been stored for this device.")
         continue
      else:
         signal_names[g] = signal_name
         break

   signal_data[g] = []
   signal_plot[g] = []
   capture_finished[g] = False
   tick_first[g] = None
   tick_last[g] = None

# Define the callback function
def cbf(GPIO, level, tick):
   # Check wether is the first edge detected
   if tick_first[GPIO] == None:
      tick_first[GPIO] = tick
      tick_last[GPIO] = tick

      # As it is the first edge, we can't calculate pulse time yet
      # The time is 0 as this edge is the starting point
       
      # When edge rising it changes from 0 to 1
      if level == 1:
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], 0, 1, ""))
         print(GPIO, device_names[GPIO], signal_names[GPIO], 0, 1, "", sep=';')
      
      # When edge falling it changes from 1 to 0
      else:
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], 0, 0, ""))
         print(GPIO, device_names[GPIO], signal_names[GPIO], 0, 0, "", sep=';')
   
   # Check wether we are still inside the capturing time window
   elif pigpio.tickDiff(tick_first[GPIO], tick) < 1e6 * args.capture_time:
      # Calculate the delta for the starting time and the pulse length
      dtick_first = pigpio.tickDiff(tick_first[GPIO], tick)
      dtick_last = pigpio.tickDiff(tick_last[GPIO], tick)
      
      # When rising it changes from 0 to 1
      if level == 1:
         signal_data[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 0, dtick_last))
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 0, dtick_last))
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 1, ""))
         print(GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 0, dtick_last, sep=';')
         print(GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 1, "", sep=';')
      
      # When falling it changes from 1 to 0
      else:
         signal_data[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 1, dtick_last))
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 1, dtick_last))
         signal_plot[GPIO].append((GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 0, ""))
         print(GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 1, dtick_last, sep=';')
         print(GPIO, device_names[GPIO], signal_names[GPIO], dtick_first, 0, "", sep=';')
      tick_last[GPIO] = tick
   
   # If it's not the first edge and we are out of the capturing window
   else:
      capture_finished[GPIO] = True

# Print the headers for the data that will be outputted
print("GPIO", "Device name", "Signal name", "Time (μs)", "Level", "Duration (μs)", sep=';')

# Add a callback for each defined GPIO pin
for g in G:
   cb[g] = pi.callback(g, pigpio.EITHER_EDGE, cbf)

# Wait for the callbacks to finish capturing data
try:
   start_time = time.time()

   while all(capture_finished.values()) == False:
      if time.time() - start_time > args.timeout:
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

# Check wether a name to save the data has been specified
if args.prefix != None:
   print("Saving the collected data")

   # Save the data for plotting the signal
   with open(args.prefix + '_plot.csv', 'w' if args.overwrite else 'a', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      if args.overwrite:
         csv_writer.writerow(["GPIO", "Device name", "Signal name", "Time (μs)", "Level", "Duration (μs)"])
      for GPIO in signal_plot:
         for signal_plot_line in signal_plot[GPIO]:
            csv_writer.writerow(signal_plot_line)
   
   # Save only the raw pulses registered
   with open(args.prefix + '_raw.csv', 'w' if args.overwrite else 'a', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      if args.overwrite:
         csv_writer.writerow(["GPIO", "Device name", "Signal name", "Time (μs)", "Level", "Duration (μs)"])
      for GPIO in signal_data:
         for signal_data_line in signal_data[GPIO]:
            csv_writer.writerow(signal_data_line)