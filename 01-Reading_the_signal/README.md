# Reading the signal
<img align="right" src="/01-Reading_the_signal/P_20240711_232829.jpg" height=200>

Equipment used:
  - Raspberry Pi 3B
  - DSO Shell D150 Oscilloscope
  - HZL-A06-B (identical to XD-RF-5V)
  - Small Breadboard
  - 2x RF Remote controls

Basics of square waveform (from www.electronics-tutorials.ws):

[![image](https://github.com/user-attachments/assets/87663d8f-73e6-47bf-94f5-0cfef6cb7e2a)](https://www.electronics-tutorials.ws/waveforms/waveforms.html)


## 2024-07-11 Getting an idea of how the signals look like
The first thing to do is just Hook up the RF module to 5V and read the signal with the oscilloscope

<img src="/01-Reading_the_signal/P_20240712_012258.jpg" height=200>

At first glance, the signal seems to be of about 1KHz and the Digital Signal Encoding looks like it could be Manchester code.
In order to acquire data from the sensor and further process it, we will try to run the receiver from the 3.3V line of the Rpi and see if we can still gather some decent signal read in the oscilloscope. For data acquisition with the Rpi we will use GPIO17.

<img src="/01-Reading_the_signal/P_20240712_021031.jpg" height=200>

The range in which the signal is picked up goes down to 1-2 cm from the coil in the receiver. But the quality of the signal at < 1 cm is as good as before. So for simplicity we will use this set-up to measure the RF signals of the remotes with the Rpi.

I am using Raspbian 12.5 (bookworm) in which the sysfs interrupts have been deprecated and removed. The alternative lgpio module does not provide enough speed and a lot of edges are missed. Pigpio (available in the repository) seems to be doing a good job though. Executing the daemon with `sudo pigpiod -s 1` to increase the sampling speed to 1μs gives a perfect resolution. To take a first glance at the data we used [the monitor.py example from Pigpio](https://abyz.me.uk/rpi/pigpio/examples.html#Python_monitor_py).

To find the first full signal I looked for a long 0 (about 12 ms), followed by 3x(1.2ms/0.6ms) 1/0 signals according to the observations in the oscilloscope (below 3 replicas of the signal, G=GPIO; l=logic state; d=duration in μs).
```
G=17 l=1 d=12243        G=17 l=1 d=12241        G=17 l=1 d=12240        
G=17 l=0 d=1218         G=17 l=0 d=1212         G=17 l=0 d=1212         
G=17 l=1 d=432          G=17 l=1 d=447          G=17 l=1 d=447          
G=17 l=0 d=1215         G=17 l=0 d=1207         G=17 l=0 d=1207         
G=17 l=1 d=450          G=17 l=1 d=451          G=17 l=1 d=451          
G=17 l=0 d=1204         G=17 l=0 d=1203         G=17 l=0 d=1204         
G=17 l=1 d=454          G=17 l=1 d=453          G=17 l=1 d=454          
G=17 l=0 d=409          G=17 l=0 d=394          G=17 l=0 d=402          
G=17 l=1 d=1235         G=17 l=1 d=1251         G=17 l=1 d=1242         
G=17 l=0 d=405          G=17 l=0 d=404          G=17 l=0 d=404          
G=17 l=1 d=1240         G=17 l=1 d=1240         G=17 l=1 d=1242         
G=17 l=0 d=404          G=17 l=0 d=405          G=17 l=0 d=403          
G=17 l=1 d=1239         G=17 l=1 d=1239         G=17 l=1 d=1241         
G=17 l=0 d=1203         G=17 l=0 d=1203         G=17 l=0 d=1201         
G=17 l=1 d=454          G=17 l=1 d=455          G=17 l=1 d=457          
G=17 l=0 d=403          G=17 l=0 d=403          G=17 l=0 d=401          
G=17 l=1 d=1247         G=17 l=1 d=1248         G=17 l=1 d=1249         
G=17 l=0 d=408          G=17 l=0 d=403          G=17 l=0 d=403          
G=17 l=1 d=1238         G=17 l=1 d=1241         G=17 l=1 d=1241         
G=17 l=0 d=1201         G=17 l=0 d=1201         G=17 l=0 d=1200         
G=17 l=1 d=457          G=17 l=1 d=460          G=17 l=1 d=459          
G=17 l=0 d=399          G=17 l=0 d=398          G=17 l=0 d=399          
G=17 l=1 d=1244         G=17 l=1 d=1242         G=17 l=1 d=1245         
G=17 l=0 d=1198         G=17 l=0 d=1207         G=17 l=0 d=1200         
G=17 l=1 d=461          G=17 l=1 d=463          G=17 l=1 d=458          
G=17 l=0 d=397          G=17 l=0 d=388          G=17 l=0 d=398          
G=17 l=1 d=1247         G=17 l=1 d=1246         G=17 l=1 d=1247         
G=17 l=0 d=1196         G=17 l=0 d=1196         G=17 l=0 d=1195         
G=17 l=1 d=470          G=17 l=1 d=453          G=17 l=1 d=461          
G=17 l=0 d=387          G=17 l=0 d=404          G=17 l=0 d=396          
G=17 l=1 d=1248         G=17 l=1 d=1248         G=17 l=1 d=1249         
G=17 l=0 d=397          G=17 l=0 d=397          G=17 l=0 d=397          
G=17 l=1 d=1251         G=17 l=1 d=1253         G=17 l=1 d=1252         
G=17 l=0 d=400          G=17 l=0 d=396          G=17 l=0 d=396          
G=17 l=1 d=1243         G=17 l=1 d=1247         G=17 l=1 d=1248         
G=17 l=0 d=400          G=17 l=0 d=400          G=17 l=0 d=397          
G=17 l=1 d=1246         G=17 l=1 d=1243         G=17 l=1 d=1247         
G=17 l=0 d=399          G=17 l=0 d=401          G=17 l=0 d=399          
G=17 l=1 d=1245         G=17 l=1 d=1244         G=17 l=1 d=1243         
G=17 l=0 d=415          G=17 l=0 d=404          G=17 l=0 d=401          
G=17 l=1 d=1229         G=17 l=1 d=1240         G=17 l=1 d=1244         
G=17 l=0 d=401          G=17 l=0 d=402          G=17 l=0 d=402          
G=17 l=1 d=1243         G=17 l=1 d=1241         G=17 l=1 d=1251         
G=17 l=0 d=402          G=17 l=0 d=404          G=17 l=0 d=393          
G=17 l=1 d=1250         G=17 l=1 d=1242         G=17 l=1 d=1243         
G=17 l=0 d=394          G=17 l=0 d=402          G=17 l=0 d=407          
G=17 l=1 d=1242         G=17 l=1 d=1243         G=17 l=1 d=1237         
G=17 l=0 d=1201         G=17 l=0 d=1199         G=17 l=0 d=1201         
G=17 l=1 d=457          G=17 l=1 d=458          G=17 l=1 d=457          
G=17 l=0 d=399          G=17 l=0 d=398          G=17 l=0 d=399          
```
A small modification of the code ([monitor_plot.py](/01-Reading_the_signal/monitor_plot.py)) allowed me to plot the signal.

<img src="/01-Reading_the_signal/power_button_signal.svg" width="100%">

After capturing 1s of the signal and averaging the length of the pulses I get 417.63 μs for the short pulses and 1231.12 μs for the long pulses.
If we assume a Manchester code the period should be twice the short pulse width and that gives a base clock frequency of 1197.61Hz ≈ 1.2KHz.
If we overlap the square wave with our signal we get quite a good overlap, although we can see that there is some jitter in the signal.

<img src="/01-Reading_the_signal/power_button_signal_wWave.svg" width="100%">

Now that we know the period and frequency, we can denoise the signal.

# 2024-07-13 Figuring out the signal
After taking a careful look to the signal, it can't be Manchester as it does not follow the rules for it (explain later)





