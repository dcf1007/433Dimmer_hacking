#!/usr/bin/env python

import time
import argparse
import csv
from pprint import pprint
import statistics

parser = argparse.ArgumentParser(description='Denoise and decode 433 MHz RF data.')
parser.add_argument('file', help='File containing the data')

args = parser.parse_args()

data = {}

with open(args.file, newline='') as csvfile:
   csv_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
   # Data has the following structure:
   # GPIO; Device name; Signal name; Time (μs); Level; Duration (μs)

   # Skip the header
   next(csv_reader)

   # Loop through the rows of data
   for row in csv_reader:
      # Set the GPIO pin nr. as key and the rest of the columns as values
      data.setdefault(row[0], []).append(row[1:])

# Define a dictionary that will contain the codeword for each GPIO pin
codewords = {}

# Loop through the different GPIO pins
for GPIO, data_GPIO in data.items():

   # Define a list to contain the different repeats of the signal captured
   codeword_repeats = []
   
   # Define a list to contain the different bits of a single signal
   codeword = []

   # Loop through the pulses captured
   for pulse in data_GPIO:
      # If the pulse is a preamble/trailing spacer pulse the codeword is complete, check and store
      if 10000 < int(pulse[5]) < 15000:
         # If the codeword is of the right length
         if len(codeword) == 24:
            # Append to the repeats
            codeword_repeats.append(codeword)
         # Empty the codeword to store the next repeat
         codeword = []
      
      # If the pulse contains the data bit plus half the sync cycle
      elif 1000 < int(pulse[5]) < 1500:
         # Add the bit value to the codeword
         codeword.append (int(pulse[4]))
      
      # If the pulse is half the sync cycle
      elif 300 < int(pulse[5]) < 500:
         # Ignore it basically
         continue
   
   # Store the consensus of the codeword repeats for the GPIO pin
   codewords[GPIO] = [statistics.mode(x) for x in zip(*codeword_repeats)]

print(codewords)
