# Capturing the commands
## 2024-07-16 Registering and decoding all the buttons
The next step is to register the signals of all the buttons of both remotes and decode them to 24-bit codewords. In order to capture the data we will use the script [monitor.py](01-Reading_the_signal/monitor_plot.py) written to read the signals. The files remote_data.csv (raw pulses) and remote_data_plot(square waves for plotting) contain the acquired raw data.
Once the signals have been acquired, we will split the different signal repetitions using the 12ms low signal, discard any blocks that contain more than 24 pulses and then do the mode of all the repetitions for each bit to filter any anomalies. The script that allows to do so is decode.py. The file remote_data_decoded.csv contains the 24-bit codewords obtained.

