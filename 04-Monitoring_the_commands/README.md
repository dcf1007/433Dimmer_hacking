# 04 - Monitoring the commands
## 2024-07-18 Receiving and identifying commands in real time

At this point we have the necessary tools to be listening in the 433 RF frequency waiting for packets of data coming from one of our receivers of interest, now we just need to write some code to do so based on the scripts created for [01 - Reading the signal](/01-Reading_the_signal):
 - Read the specified GPIOs every 1 µs
 - Ignore all pulses shorter than 300 µs
 - Record signals if there has been an idle low period of 10 ms
 - If after receiving 25 pulses it doesn't go silent for at least 10 ms, ignore
 - Check for a second repetition and compare. If both repeats match, compare against known commands

The resulting script is [monitor.py](/04-Monitoring_the_commands/monitor.py). We can now automate both receiving signals from the remote and execute an action, or send actions to the receiver.

The final step will be 
