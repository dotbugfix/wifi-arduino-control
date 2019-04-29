# WiFi Arduino Control
A reference project that uses the ESP8266 microchip to establish a 2-way communication channel between a Python-based server and an Arduino board. The comms are HTTP-based and use RESTful APIs to get/push data to/from the Arduino board.

## Microcontroller
This project was built using the WeMos D1 development board for ESP8266 which is based on Arduino. The Arduino IDE can be used to flash the microcode onto the board by adding it as a 3rd party board, which will also install the required libraries and headers for ESP8266.

> See the tutorial for [WeMos D1](https://cyaninfinite.com/getting-started-with-the-wemos-d1-esp8266-wifi-board/) for setting it up

## Backend Server
A Python Flask app serves the RESTful API to communicate with the board. This can be deployed locally on the same WiFi network or hosted on a public cloud server with a known URL. The only requirement is for the Arduino board to connect to a WiFi network that can access this server.

## Demo
The following content demonstrates the end-to-end execution of the solution. It is exactly reproducible with your own Arduino board with a ESP8266 chip and any system hosting the Python server.

### Server -> Microcontroller (LED toggle)
1. Flash the Arduino sketch to the microcontroller and start the serial monitor to view debug messages emitted by the program. Make sure to change `arduino/wifi_sketch/config.h` with real values of the WiFi Access Point SSID and password before flashing.

```
[WiFi] Connecting to SSID ItzAlive!.....
[WiFi] Connected to 'ItzAlive!' with IP address: 192.168.43.61
[WiFi] mDNS responder registered for domain name: esp8266
[HTTP] server started
```

2. Start the Python server with the IP address of the microcontroller.

```
$ python server.py 192.168.43.61
INFO     | 
WiFi Arduino Control v0.1.0 beta released on 28-Apr-2019
=============================
OS: Linux-4.15.0-45-generic-x86_64-with-Ubuntu-18.04-bionic
Python: 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0]
System: <snip>
Working directory: <snip>
Runtime path: <snip>
Commandline: server.py 192.168.43.61
=============================
Log file: <snip>
=============================
    
INFO     | Creating a new instance of Arduino Device with IP: 192.168.43.61
INFO     | HTTP server starting on: http://localhost:5000
```

3. Using a web browser, verify that the Python server is accepting HTTP requests by making a GET request on `http://localhost:5000/api/version`. The server will record this request in its log file:

```
INFO     | 127.0.0.1 - - [29/Apr/2019 08:40:03] "GET /api/version HTTP/1.1" 200 -
```

4. Now make a GET request on `http://localhost:5000/api/server/led/toggle` which will in turn make an HTTP GET request on `http://<microcontroller_ip>/api/device/led/toggle` that is handled by the HTTP server on the ESP8266 chip and toggles the state of the on-board LED. The server will record these actions in its log file.

```
INFO     | Toggle the LED on device: ArduinoDevice<IP:192.168.43.61>
INFO     | Making a HTTP GET request on http://192.168.43.61/api/device/led/toggle
INFO     | Response: b'{"success": true}'
INFO     | 127.0.0.1 - - [29/Apr/2019 08:53:08] "GET /api/server/led/toggle HTTP/1.1" 200 -
```

5. You can also directly make an HTTP GET request on `http://<microcontroller_ip>/api/device/led/toggle` using a web browser to have the same effect on the microcontroller, which can be seen on the serial monitor.

```
[HTTP][Request] GET on /api/device/led/toggle
LED state is now 1
[HTTP][Response] GET on /api/device/led/toggle: 200
```

Each HTTP request will toggle the state of the LED from ON to OFF and vice-versa.


### Microcontroller -> Server (Report device readings)
_(follow steps 1-3 above)_

4. The microcontroller is setup to send a hypothetical reading (as if a sensor were connected to it) every 1 second to the server by making an HTTP POST request on `http://<server_ip>/api/device/data` with a payload containing the reading value.

   (a) This can be observed on the microcontroller's serial monitor:
   ```
    [HTTP_Client] Sending reading 7 to server http://192.168.43.116:5000/api/device/data
    [HTTP_Client] Sending reading 48 to server http://192.168.43.116:5000/api/device/data
    [HTTP_Client] Sending reading 14 to server http://192.168.43.116:5000/api/device/data
   ```

   (b) The request is also recorded in the Python server's log file (seen on stdout):
   ```
    INFO     | Data from device: {'reading': 7}
    INFO     | 192.168.43.61 - - [29/Apr/2019 08:53:09] "POST /api/device/data HTTP/1.1" 200 -
   ```

Both communications are handled simultaneously since the Python server and the microcontroller both act as an HTTP client and an HTTP server at the same time.