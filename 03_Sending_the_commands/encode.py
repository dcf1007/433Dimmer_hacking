#!/usr/bin/env python

import argparse
import pigpio
import time

parser = argparse.ArgumentParser(description='Encode 433 MHz RF data.')
parser.add_argument('GPIO', type=int, nargs=1, help='GPIO pins to send the signal')
parser.add_argument('--codeword', required=True, help='24-bit codeword in binary')
parser.add_argument('-f', '--frequency', type=int, default=1200, help='Clock frequancy')
parser.add_argument('-r', '--repeats', type=int, default=16, help='Number of times the signal gets sent in a row')
#parser.add_argument('-s', '--structure', default="[LH]24[DDLH]14[LL]", help='Structure of the data packet to send the signal')

args = parser.parse_args()

# Define GPIO pin
gpio_pin = args.GPIO

# Set the clock frequency
frequency = args.frequency

# Calculate the pulse width (1/2 clock cycle) for the frequency.
# In micro-seconds. FLOAT
pulse_width = 5e5/frequency 

# Set the 24-bit codeword to send.
# Check it is 24-bit and in binary
codeword = args.codeword if (len(args.codeword) == 24 and set(args.codeword) <= set(["0", "1"])) else exit("Not a valid codeword")

# Set the number of times the signal will be sent
nr_repeats = args.repeats 

# Initialize pigpio
pi = pigpio.pi()

# Exit if the daemon is not in execution
if not pi.connected:
   exit()


# Define the signals
def H_signal(nr_pulses=1):
   return pigpio.pulse(1<<gpio_pin, 0, int(pulse_width * nr_pulses))

def L_signal(nr_pulses=1):
   pigpio.pulse(0, 1<<gpio_pin, int(pulse_width * nr_pulses))

# List to store the sequence of signals to send
signal = []

# Add the [LH] period
signal.extend([L_signal(), H_signal()])

# Add the 24[DDLH] blocks
for bit in codeword:
    if bit == "1":
        signal.append(H_signal(2)) # Data period DD
    else:
        signal.append(L_signal(2)) # Data period DD
    
    signal.extend([L_signal(), H_signal()]) # Clock period LH

# Add the 14[LL] block
signal.append(L_signal(14))

# Clear any existing waveforms
pi.wave_clear()  

# Create a new waveform using the pulse sequence
pi.wave_add_generic(signal)

# Get the waveform ID
signal_wave_id = pi.wave_create()

# Create the chain that will send the signal repeated several times
# 255,0 -> Start of a loop
# 255,1,<nr>,0 -> End of a loop of <nr> repeats
signal_chain = [255, 0, signal_wave_id, 255, 1, nr_repeats, 0]

# Send the waveform containing the signal
pi.wave_chain(signal_chain)
#pi.wave_send_once(wave_id)
#pi.wave_send_repeat(wave_id)

# Wait for the transmission to finish
while pi.wave_tx_busy():
   time.sleep(0.1)

# Clean up
pi.wave_delete(signal_wave_id)  # Delete the waveform
pi.stop()  # Disconnect from pigpio