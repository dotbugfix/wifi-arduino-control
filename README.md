# WiFi Arduino Control
A reference project that uses the ESP8266 microchip to establish a 2-way communication channel between a Python-based server and an Arduino board. The comms are HTTP-based and use RESTful APIs to get/push data to/from the Arduino board.

## Microcontroller
This project was built using the WeMos D1 development board for ESP8266 which is based on Arduino. The Arduino IDE can be used to flash the microcode onto the board by adding it as a 3rd party board, which will also install the required libraries and headers for ESP8266.

> See the tutorial for [WeMos D1](https://cyaninfinite.com/getting-started-with-the-wemos-d1-esp8266-wifi-board/) for setting it up

## Backend Server
A Python Flask app serves the RESTful API to communicate with the board. This can be deployed locally on the same WiFi network or hosted on a public cloud server with a known URL. The only requirement is for the Arduino board to connect to a WiFi network that can access this server.