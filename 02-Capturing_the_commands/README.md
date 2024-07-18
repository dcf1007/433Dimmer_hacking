# Capturing the commands
## 2024-07-16 Registering and decoding all the buttons
The next step is to register the signals of all the buttons of both remotes and decode them to 24-bit codewords.

In order to capture the data we will use the script [monitor_plot.py](/01-Reading_the_signal/monitor_plot.py) written to read the signals in [01 - Reading the signal](/01-Reading_the_signal). The files [data_remotes_raw.csv](/02-Capturing_the_commands/data_remotes_raw.csv) (raw pulses) and [data_remotes_plot.csv](/02-Capturing_the_commands/data_remotes_plot.csv) (square waves for plotting) contain the acquired raw data.

With the acquired raw pulse data, we will do the following processing using the script [decode.py](/02-Capturing_the_commands/decode.py):
 - Split the different signal repeats using the 12ms low signal
 - Append to the codeword the level of the pulses with 1.2ms (and ignore the 0.4 ms clock pulses)
 - Discard any codeword repeats that contain more than 24 pulses
 - Apply the mode to all the repetitions for each bit to filter any anomalies
 - Store the consensus codeword

 The file [data_remotes_decoded.csv](/02-Capturing_the_commands/data_remotes_decoded.csv) contains the 24-bit codewords obtained.

|              | remote_a                       | remote_b                       |
|--------------|--------------------------------|--------------------------------|
| on_off_btn   | **0111100100000011**_00000001_ | **1110001001010100**_00000001_ |
| light_btn    | **0111100100000011**_00000100_ | **1110001001010100**_00000100_ |
| bright_plus  | **0111100100000011**_00000101_ | **1110001001010100**_00000101_ |
| bright_minus | **0111100100000011**_00000110_ | **1110001001010100**_00000110_ |
| bright_100   | **0111100100000011**_00000111_ | **1110001001010100**_00000111_ |
| bright_50    | **0111100100000011**_00001000_ | **1110001001010100**_00001000_ |
| bright_25    | **0111100100000011**_00001001_ | **1110001001010100**_00001001_ |
| mode_plus    | **0111100100000011**_00001011_ | **1110001001010100**_00001011_ |
| mode_minus   | **0111100100000011**_00010001_ | **1110001001010100**_00010001_ |
| speed_plus   | **0111100100000011**_00001111_ | **1110001001010100**_00001111_ |
| speed_minus  | **0111100100000011**_00001101_ | **1110001001010100**_00001101_ |
| pair_signal  | **0111100100000011**_00111111_ | **1110001001010100**_00111111_ |

In bold you can see the remote ID and in italics the command. All commands for both remotes match, whilst all the remote IDs match for all the commands of one remote.

Next is:  [03 - Sending the commands](/03-Sending_the_commands)
