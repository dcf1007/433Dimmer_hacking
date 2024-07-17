#!/usr/bin/env python

import pigpio
import time

frequency = 1200
pulse_width = 5e5/frequency # In micro-seconds. 1/2 clock cycle. FLOAT
codeword = "111111111111111100000001" # The 24-bit codeword to send
nr_repeats = 16 # Set the number of times the signal will be sent

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    exit()

# Define GPIO pin
gpio_pin = 17  # Example GPIO pin

# The three different types of periods we can have
HH_period  = [pigpio.pulse(1<<gpio_pin, 0, int(2*pulse_width)), ]
LL_period  = [pigpio.pulse(0, 1<<gpio_pin, int(2*pulse_width)), ]
LH_period = [pigpio.pulse(0, 1<<gpio_pin, int(pulse_width)), pigpio.pulse(1<<gpio_pin, 0, int(pulse_width))]


# List to store the sequence of pulses to send
pulse_signal = []

# Data packet structure: [LH]24[DDLH]14[LL]

# Add the [LH] period
pulse_signal.extend(LH_period)

# Add the 24[DDLH] blocks
for bit in codeword:
    if bit == "1":
        pulse_signal.extend(HH_period) # Data period DD
    else:
        pulse_signal.extend(LL_period) # Data period DD
    
    pulse_signal.extend(LH_period) # Clock period LH

# Add the 14[LL] block
pulse_signal.extend(LL_period*14)

# Clear any existing waveforms
pi.wave_clear()  

# Create a new waveform using the pulse sequence
pi.wave_add_generic(pulse_signal)

# Get the waveform ID
signal_wave_id = pi.wave_create()

# Create the chain that will send the signal repeated several times
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