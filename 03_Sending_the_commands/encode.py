import pigpio
import time

frequency = 1200
pulse_width = 5e5/frequency # 1/2 clock cycle. FLOAT
#long_pulse = int(1e6/frequency) # 1 clock cycle
#pause_pulse = int(14e6/frequency) # 14 clock cycles

codeword = "111000100101010000000001"
pulse_signal = []

# Initialize pigpio
pi = pigpio.pi()

if not pi.connected:
    exit()

# Define GPIO pin
gpio_pin = 17  # Example GPIO pin
'''
# Clock period
pulse_signal.append(pigpio.pulse(0, 1<<gpio_pin, short_pulse))
pulse_signal.append(pigpio.pulse(1<<gpio_pin, 0, short_pulse))
'''

H_period  = [pigpio.pulse(1<<gpio_pin, 0, int(2*pulse_width)), ]
L_period  = [pigpio.pulse(0, 1<<gpio_pin, int(2*pulse_width)), ]
HL_period = [pigpio.pulse(1<<gpio_pin, 0, int(pulse_width)), pigpio.pulse(0, 1<<gpio_pin, int(pulse_width))]
LH_period = [pigpio.pulse(0, 1<<gpio_pin, int(pulse_width), pigpio.pulse(1<<gpio_pin, 0, int(pulse_width)))]

# Pause pulse
pulse_signal.append(pigpio.pulse(0, 1<<gpio_pin, pause_pulse))

for bit in codeword:
    if bit == "1":
        # Data pulse
        pulse_signal.append()

        # Clock period
        pulse_signal.append(pigpio.pulse(1<<gpio_pin, 0, short_pulse))
        pulse_signal.append(pigpio.pulse(0, 1<<gpio_pin, short_pulse))
        
    else:
        # Data pulse
        pulse_signal.append(pigpio.pulse(0, 1<<gpio_pin, long_pulse))
        
        # Clock period
        pulse_signal.append(pigpio.pulse(1<<gpio_pin, 0, short_pulse))
        pulse_signal.append(pigpio.pulse(0, 1<<gpio_pin, short_pulse))
        

# Create a wave using the pulse
pi.wave_clear()  # Clear any existing waveforms
pi.wave_add_generic(pulse_signal)  # Add the pulse to the waveform

# Get the waveform ID
wave_id = pi.wave_create()

chain = [255, 0, wave_id, 255, 1, 1, 0]

#pi.wave_send_once(wave_id)
pi.wave_chain(chain)

#pi.wave_send_repeat(wave_id)

while pi.wave_tx_busy():
   time.sleep(0.1)

# Clean up
pi.wave_delete(wave_id)  # Delete the waveform
pi.stop()  # Disconnect from pigpio