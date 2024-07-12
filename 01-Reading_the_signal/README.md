# Reading the signal
<img align="right" src="/01-Reading_the_signal/P_20240711_232829.jpg" height=200>

Equipment used:
  - Raspberry Pi 3B
  - DSO Shell D150 Oscilloscope
  - HZL-A06-B (identical to XD-RF-5V)
  - Small Breadboard
  - 2x RF Remote controls

## 2024-07-11 Getting an idea of how the signals look like
The first thing to do is just Hook up the RF module to 5V and read the signal with the oscilloscope

<img src="/01-Reading_the_signal/P_20240712_012258.jpg" height=200>

At first glance, the signal seems to be of about 1KHz and the Digital Signal Encoding looks like it could be Manchester code.
In order to acquire data from the sensor and further process it, we will try to run the receiver from the 3.3V line of the Rpi and see if we can still gather some decent signal read in the oscilloscope. For data acquisition with the Rpi we will use GPIO17.

<img src="/01-Reading_the_signal/P_20240712_021031.jpg" height=200>

The range in which the signal is picked up goes down to 1-2 cm from the coil in the receiver. But the quality of the signal at < 1 cm is as good as before. So for simplicity we will use this set-up to measure the RF signals of the remotes with the Rpi

