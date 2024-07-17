#!/usr/bin/env python

import argparse
import csv
import statistics

parser = argparse.ArgumentParser(description='Denoise and decode 433 MHz RF data.')
parser.add_argument('file_in', help='File containing the data')
parser.add_argument('file_out', help='File to store the 24-bit codewords')

args = parser.parse_args()

data = {}

with open(args.file_in, newline='') as csvfile:
   csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   # Data has the following structure:
   # GPIO; Device name; Signal name; Time (μs); Level; Duration (μs)

   # Skip the header
   next(csv_reader)

   # Loop through the rows of data
   for row in csv_reader:
      # In this case the GPIO pin is not important anymore.
      # Select the name of the device as key of the main dict.
      # The value of the dict is another dict which will have as key
      # The command name and as value the level and duration of the pulse
      data.setdefault(row[1], {}).setdefault(row[2], []).append(row[4:])

# Define a dictionary that will contain the codeword for each GPIO pin
codewords = {}

# Define lists to store allnames for the devices and signals to create the final table
device_names = []
signal_names = []

# Loop through the different devices
for device_name, device_data in data.items():
   # Store the device name
   device_names.append(device_name)

   # Loop through all the different signals for the device
   for signal_name, signal_pulses in device_data.items():
      # Store the signal name
      signal_names.append(signal_name)

      # Define a list to contain the different repeats of the signal captured
      codeword_repeats = []
      
      # Define a list to contain the different bits of a single signal
      codeword = []

      # Loop through the pulses captured
      for pulse in signal_pulses:
         # If the pulse is a preamble/trailing spacer pulse the codeword is complete, check and store
         if 10000 < int(pulse[1]) < 15000:
            # If the codeword is of the right length
            if len(codeword) == 24:
               # Append to the repeats
               codeword_repeats.append(codeword)
            # Empty the codeword to store the next repeat
            codeword = []
         
         # If the pulse contains the data bit plus half the sync cycle
         elif 1000 < int(pulse[1]) < 1500:
            # Add the bit value to the codeword
            codeword.append (int(pulse[0]))
         
         # If the pulse is half the sync cycle
         elif 300 < int(pulse[1]) < 500:
            # Ignore it basically
            continue
      
      # Store the consensus of the codeword repeats for each device and signal
      codewords.setdefault(device_name, {})[signal_name] = "".join([str(statistics.mode(x)) for x in zip(*codeword_repeats)])


# Save only the raw pulses registered
with open(args.file_out, 'w', newline='') as csvfile:
   csv_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
   csv_writer.writerow(["", *[x for x in device_names]])
   for signal in signal_names:
      csv_writer.writerow([signal, *[x.get(signal, " "*24) for x in codewords.values()]])
