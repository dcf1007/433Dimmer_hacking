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

There is a mixture of short and long pulses. At first glance, if we assume the shortest pulse to be the pulse width of the signal, it seems to be of about 1KHz and the Digital Signal Encoding looks like it could be Manchester code.
In order to acquire data from the sensor and further process it, we will try to run the receiver from the 3.3V line of the Rpi and see if we can still gather some decent signal read in the oscilloscope. For data acquisition with the Rpi we will use GPIO17.

<img src="/01-Reading_the_signal/P_20240712_021031.jpg" height=200>

The range in which the signal is picked up goes down to 1-2 cm from the coil in the receiver. But the quality of the signal at < 1 cm is as good as before. So for simplicity we will use this set-up to measure the RF signals of the remotes with the Rpi.

In Raspbian 12.5 (bookworm),  the sysfs interrupts have been deprecated and removed. The alternative lgpio module does not provide enough speed and a lot of edges are missed. Pigpio (available in the repository) seems to be doing a good job though. Executing the daemon with `sudo pigpiod -s 1` to increase the sampling speed to 1μs gives a perfect resolution. To take a first acquisition we used [the monitor.py example from Pigpio](https://abyz.me.uk/rpi/pigpio/examples.html#Python_monitor_py).

To find the first full signal we looked for a long low (about 12 ms), followed by 3 x (1.2ms/0.6ms) high/low signals according to the observations in the oscilloscope (below 3 replicas of the signal, G=GPIO; l=edge direction; d=duration in μs). Bear in mind that for example `G=17 l=1 d=12243` does not indicate that there were 12ms in state high, but that there was a change from low to high after 12ms, therefore the 12 ms were LOW.
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
Taking that script as basis, and With some modifications we wrote the script ([capture.py](/01-Reading_the_signal/capture.py)) which will both save the raw pulses detected and provide an extra file to plot the signal.

<img src="/01-Reading_the_signal/raw_signal.svg" width="100%">

After capturing 1s of the signal (19 full repetitions), we averaged the values and calculated the midrange and the maximum deviation:
|                | Geo. Mean | Midrange | Max. dev |
|----------------|-----------|----------|----------|
| Short pulse    | 417.0     | 428.0    | 50.0     |
| Short pulse    | 1229.8    | 1220.5   | 49.5     |
| Preamble pulse | 12240.0   | 12241.0  | 10.0     |

The length of the long pulses seems to be 3 times the duration of the short pulses and they seem to jitter about ± 50 μs.
If we assume that it uses Manchester code, the period should be twice the width of the short pulse and that gives a base clock frequency of 1199 Hz ≈ 1.2KHz.
Now we can overlap the square wave with our signal and see if they fit. We get quite a good overlap, although we can see that the jitter in the signal and because of it, by the end of the signal we have lost a full pulse width.

<img src="/01-Reading_the_signal/raw_signal_w_clock.svg" width="100%">

Knowing the frequency, now we can denoise the signal to get rid of the jitter before continuing the analysis. For that we divide the duration of each pulse by the average duration of the short pulse, round it to the closest integer and multiply it by the theoretical pulse width of 1.2 KHz.

<img src="/01-Reading_the_signal/denoised_signal_w_clock.svg" width="100%">


# 2024-07-13 Figuring out the signal
After taking a careful look to the signal, it can't be Manchester as it does not follow the rules for it.

<img src="https://github.com/user-attachments/assets/3257fa26-7c50-46ed-b010-aa060b38eaff" height=200>

In Manchester code, the period for 1 is `[LH]` (the first half period is a low pulse and the second half period high pulse), and for 0 is `[HL]` (the first half period is a high pulse and the second half period is a low pulse). In this signal we can identify 3 different periods, `[HH]` (all high), `[LL]` (all low), `[LH]` (pulse low and second pulse high).

<img src="https://github.com/user-attachments/assets/43972934-5c6c-4257-ac76-95f428a97822" height=200>

That reminded me of CMI (Coded Mark Inversion). In CMI the 0 is always `[LH]` while the 1 alternates between `[LL]` and `[HH]` each time it is coded. The signal of the remote would break the alternating rule.

There seems to be a pattern in the remote signal though, after each period `[HH]` or `[LL]` comes a `[LH]` inconditionally.

# 2024-07-15 Decoding the signal
So following with the previous assumption, it would seem that after every period containing data there is a period with a clock tick before the next data period (every second period is a clock tick). So Period A = 0, Period B = 1 and Period C = Clock tick.

<img src="/01-Reading_the_signal/decoded_signal.svg" width="100%">

Reading it this way, it gives us 24-bit codeword: `111000100101010000000001`. This codeword belongs to the ON/OFF button of one of the remotes. 
In order to try to figure out which bits are the remote ID and which ones are the command, we can read the second remote and look at which bits are invariable.

<img src="/01-Reading_the_signal/raw_signal_second_remote.svg" width="100%">

```
         | 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
---------|-----------------------------------------------------------------------
Remote A | 1  1  1  0  0  0  1  0  0  1  0  1  0  1  0  0  0  0  0  0  0  0  0  1
Remote B | 0  1  1  1  1  0  0  1  0  0  0  0  0  0  1  1  0  0  0  0  0  0  0  1
           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
                            Remote ID                              Command
```
The first 16 bit seem to be the ID of the remote and vary between them whilst the last 8 bit seem to be the command

## 2024-07-17 Preamble and tail
At this point we can extract the data, but we can't recreate the exact data packet as we have not determined the preamble and the tail of the package. The signal repeats itself indefinitely and each signal is separated from each other by 14 LL periods.

If we look at the leading 14 LL periods, we see that there is a LH right before the first data period. So the whole data packet would be:
`14[LL][LH]24[DDLH]` where DD is the data (either LL or HH).

The 14[LL] could also be a tail and the first [LH] be the preamble `[LH]24[DDLH]14[LL]` or everything could be tail `24[DDLH]14[LL][LH]`.

We previously assumed that the clock period was positioned **after** each data period, but as there is also a clock period before the first data period, the following structure could also be correct `14[LL]24[LHDD][LH]`. 

And if we assume the latter structure, the last [LH] could also be part of the preamble instead `[LH]14[LL]24[LHDD]`. In the same way, the 14[LL] could be part of the tail, and no preamble `24[LHDD][LH]14[LL]`.

That leaves us with 6 possible valid data structures, from which 4 are unique combinations: `[LH]14[LL]24[LHDD]`, `24[LHDD][LH]14[LL]` == `[LH]24[DDLH]14[LL]`, `14[LL]24[LHDD][LH]` == `14[LL][LH]24[DDLH]`, 
`24[DDLH]14[LL][LH]`. The equivalent ones can have different ways to divide it, but same final package structure.

<img src="/01-Reading_the_signal/packet_possibilities.svg" width="100%">

The only way to know which one is the right packet structure is by sending a single packet of each of the combinations and hoping that the receiver only reacts to one of them. That will be dealt with in [03 - Sending the commands](/03-Sending_the_commands)

Next is: [02 - Capuring the commands](/02-Capturing_the_commands)
