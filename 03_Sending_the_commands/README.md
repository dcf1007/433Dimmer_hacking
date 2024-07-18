# Sending the commands
<img align="right" src="/03_Sending_the_commands/P_20240718_065040.jpg" height=200>

Equipment used:
  - Raspberry Pi 3B
  - The transmitter module: FS1000a
  - Small Breadboard
  - 1x RF LED dimmer
  - Small LED strip


## 2024-07-17
In [01 Reading the signal](/01-Reading_the_signal) we commented that the packet structure could be formed in several different ways. We will now try to figure out the correct structure to send the message.

A small recap of the possible combinations:
<img src="/01-Reading_the_signal/packet_possibilities.svg" width="100%">

In order to send the commands we wrote the script [encode.py](/03-Sending_the_commands/encode.py):
 - It takes the specified 24-bit codeword
 - It creates the pulses for the data packet and adds the data pulses to it
 - It creates a square wave made of the list of pulses given
 - It sends the wave n number of times in a row

Before starting any attempts, we manually bring the level of the emitter low/high/low in intervals of 1s to make sure to reset any waiting in the receiver

These are the results for the 4 possible data packet structures:
 - Data structure `24[DDLH]14[LL][LH]`
    - The _first command_ is **always** ignored, no matter if the initial idle level is high or low.
    - It reacts to the _second command_ sent and every single one following **if the emitter keeps the level high after sending**.
      If you bring the level to low then it won't recognize the second command either, or any other following.
    - It seems that when it receives either the `[LH]` or the `14[LL][LH]` the receiver continues awaiting for the rest of the command
 - Data structure `14[LL][LH]24[DDLH]` == `14[LL]24[LHDD][LH]`
    - The _first and second commands_ are **always** ignored.
    - It reacts to the _third command_ sent and every single one following **if the emitter keeps the level high after sending**
      If you bring the level to low then it won't recognize the third command either, or any other following.
    - It looks like the preamble is not completed until the second time the command is sent, and then it stays awaiting for the rest of the command
 - Data structure `24[LHDD][LH]14[LL]` = `[LH]24[DDLH]14[LL]`
    - It **never** reacts. No matter if the idle state is high or low, and wether you set the idle level after the signal to high or low.
    - It looks like it never receives the whole preamble in a way it can wait for the rest of the command
 - Data structure `[LH]14[LL]24[LHDD]`
    - The _first and second commands_ are **always** ignored.
    - It reacts to the _third command_ sent and every single one following **if the emitter keeps the level high after sending**
      If you bring the level to low then it won't recognize the third command either, or any other following.
    - It looks like the preamble is not completed until the second time the command is sent, and then it stays awaiting for the rest of the command

The results were rather inconclusive and insatisfactory. We then tried to isolate the beginning of the signal from the original remote by manually pressing shortly the power button and releasing it to get the shortest pulse possible.

The shortest pulse we managed to generate consisted of 2 repeats, leading and trailing idle low:
 - There are no signs of an `[LH]` before `14[LL]`
 - From reading remote A, which starts with a bit 0, we see that the signal contains `[LH]` before the first `[DD]`
 - There is an `[LH]` after the last `[DD]` in the first repeat followed by `14[LL]`

The pattern we got from the remotes was `[LH]24[DDLH]14[LL][LH]24[DDLH]` and idle low after (probably `14[LL]` was sent too). It corresponds to the structure that never reacted when sent individually. Sending it only once, it never reacts. Sending it twice, it always reacts.

Now we have a way to send signals to the receiver. The last step is to monitor the messages from the RF remote and identify which button was pressed in real time.

Next: [04 - Monitoring the commands](/04-Monitoring_the_commands)
