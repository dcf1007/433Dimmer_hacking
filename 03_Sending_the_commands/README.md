# Sending the commands
## 2024-07-17
Before starting, we bring the level low/high/low in intervals of 1s to make sure to reset any waiting in the receiver
 - Data structure 24[DDLH]14[LL][LH]
    - The _first command_ is **always** ignored, no matter if the initial idle level is high or low.
    - It reacts to the _second command_ sent and every single one following **if the emitter keeps the level high after sending**.
      If you bring the level to low then it won't recognize the second command either, or any other following.
    - It seems that when it receives either the [LH] or the 14[LL][LH] the receiver continues awaiting for the rest of the command
 - Data structure 14[LL][LH]24[DDLH] == 14[LL]24[LHDD][LH]
    - The _first and second commands_ are **always** ignored.
    - It reacts to the _third command_ sent and every single one following **if the emitter keeps the level high after sending**
      If you bring the level to low then it won't recognize the third command either, or any other following.
    - It looks like the preamble is not completed until the second time the command is sent, and then it stays awaiting for the rest of the command
 - Data structure 24[LHDD][LH]14[LL] = [LH]24[DDLH]14[LL]
    - It **never** reacts. No matter if the idle state is high or low, and wether you set the idle level after the signal to high or low.
    - It looks like it never receives the whole preamble in a way it can wait for the rest of the command
 - Data structure [LH]14[LL]24[LHDD]
    - The _first and second commands_ are **always** ignored.
    - It reacts to the _third command_ sent and every single one following **if the emitter keeps the level high after sending**
      If you bring the level to low then it won't recognize the third command either, or any other following.
    - It looks like the preamble is not completed until the second time the command is sent, and then it stays awaiting for the rest of the command

The results were rather inconclusive and insatisfactory. We then tried to isolate a the beginning of the signal from the original remote as well as sending the shortest pulse possible.

The shortest pulse generated consisted of 2 repeats, leading and tailing idle low:
 - There are no signs of an [LH] before 14[LL]
 - From reading remote A, which starts with a bit 0, we see that the signal contains [LH] before the first [DD]
 - There is an [LH] after the last [DD] in the first repeat followed by 14[LL]
The pattern we got from the remotes was [LH]24[DDLH]14[LL][LH]24[DDLH] and idle low after (probably 14[LL] is sent too). It corresponds to the structure that never reacted when sent individually. After sending it twice, it always reacts.
