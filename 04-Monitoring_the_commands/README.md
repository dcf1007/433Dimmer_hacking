# 04 - Monitoring the commands
At this point we have the necessary tools to be listening in the 433 RF frequency waiting for packets of data coming from one of our receivers of interest, now we just need to write some code to:
 - Read the specified GPIOs every 1 µs
 - Ignore all pulses shorter than 300 µs
 - Record signals if there has been an idle low period of 10 ms
 - If after receiving 25 pulses it doesn't go silent for at least 10 ms, ignore
 - Check for a second repetition and compare. If both repeats match, compare against known commands
## 2024-07-18 Draft of the code
Implemented first version of the code based on the scripts created for [01 - Reading the signal](/01-Reading_the_signal)
The resulting script is [monitor.py](/04-Monitoring_the_commands/monitor.py)

## 2024-07-23 Receiving commands in real time
The script is now able to continuously monitor, identify the start of a data packet, receive repeats and generate a consensus code for the received signal in real time

## 2024-07-24 Receiving and identifying commands in real time
Removed creating the consensus for the repeats. There are some buttons which should react to every repeat. For example if we keep the brightness buttons pressed. 

Implemented the functionality to identify a saved remote and check the received command against the list of saved commands generated with [decode.py](/02-Capturing_the_commands/decode.py)
