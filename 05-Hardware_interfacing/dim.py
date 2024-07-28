#!/usr/bin/env python

import pigpio
import time

# Define GPIO pin
gpio_pin = 17

# Set the clock frequency
frequency = 300

# Calculate the pulse width frequency.
# In micro-seconds. FLOAT
pulse_width = 1e6/frequency 

# Initialize pigpio
pi = pigpio.pi()

# Exit if the daemon is not in execution
if not pi.connected:
   exit()

# Define the dimming signal
def signal(percentage):
   print(round(percentage,2), "\t", round(pulse_width * percentage/100), "\t", round(pulse_width * (100-percentage)/100))
   return [pigpio.pulse(0, 1<<gpio_pin, round(pulse_width * (100-percentage)/100)), pigpio.pulse(1<<gpio_pin, 0, round(pulse_width * percentage/100))]*10
# Clear any existing waveforms
pi.wave_clear()

# At least 2, 0% and 100%
dim_steps = 100

# Create the lsit to contain the pulses of signal wave
signal_wave = []

# Dimming steps when the exponential is less than 1
dim_steps_lt1 = round(dim_steps*0.1)

# Dimming steps when the exponential is greater than 1
dim_steps_gt1 = dim_steps - dim_steps_lt1 - 1

# Base for the exponential
dim_base =  100**(1/(dim_steps_gt1)) if dim_steps > 0 else 100

dim_step = 0
while dim_step < dim_steps:
   if dim_step == 0:
      signal_wave.extend(signal(0))
   elif dim_step < dim_steps_lt1:
      signal_wave.extend(signal(dim_step/dim_steps_lt1))
   else:
      signal_wave.extend(signal(dim_base**(dim_step - dim_steps_lt1)))
   dim_step += 1

pi.wave_add_generic(signal_wave)
signal_wave_id = pi.wave_create()
signal_chain = [255, 0, signal_wave_id, 255, 1, 1, 0]
pi.wave_chain(signal_chain)


# Wait for the transmission to finish
while pi.wave_tx_busy():
   time.sleep(0.1)

# Clean up
pi.wave_delete(signal_wave_id)  # Delete the waveform
pi.stop()  # Disconnect from pigpio
