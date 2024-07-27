# 05 - Hardware interfacing

## 2024-07-27 Designing the interface
The LED strips work at a voltage of 12-24 V and high current. The GPIO ports of the raspberry pi and ESP8266/ESP32 work at 3.3 V and very low current. We need to create an interface that allow us to connect both ends together.

In order to drive the LED strips we will be using an LED amplifier, which has a power supply input, a PWM input and an LED output. This way, we just need to supply a PWM signal with low current to the amplifier, and it will take care of driving the LED strips at high current. On the other side, we still have the voltage difference. To overcome that we will use a simple unidirectional voltage shifter using a BJT NPN transistor 2N2222. A good summary with nice diagrams can be found in this post of Electrical Engineering Stack Exchange: [Logic level converter using Transistors](https://electronics.stackexchange.com/q/296879)

<img src="/05-Hardware_interfacing/unidirectional_voltage_level_shifter.svg" height=200>
