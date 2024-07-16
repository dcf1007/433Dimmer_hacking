# Capturing the commands
## 2024-07-16 Registering and decoding all the buttons
The next step is to register the signals of all the buttons of both remotes and decode them to 24-bit codewords. In order to capture the data we will use the script [monitor.py](../01-Reading_the_signal/monitor_plot.py) written to read the signals. The files data_remotes_raw.csv (raw pulses) and data_remotes_plot.csv (square waves for plotting) contain the acquired raw data.
Once the signals have been acquired, we will split the different signal repetitions using the 12ms low signal, discard any blocks that contain more than 24 pulses and then do the mode of all the repetitions for each bit to filter any anomalies. The script that allows to do so is decode.py. The file data_remotes_decoded.csv contains the 24-bit codewords obtained.

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

In bold you can see the remote ID and in italics the command
