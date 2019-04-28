#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include "config.h"

ESP8266WebServer server(80);

const int led = LED_BUILTIN;
int LED_STATE = 0;

/**
 * Service handler for '/'
 * 
 * Send a simple 'hello' message as plain text
 */
void handleRoot() {
  Serial.println("[HTTP][Request] GET on /");
  server.send(200, "text/plain", "Hello, World!");
  Serial.println("[HTTP][Response] GET on /: 200");
}

/**
 * Service handler for unknown URLs
 */
void handleNotFound()
{
  String message = "Unknown API:nn";
  message += "URI: ";
  message += server.uri();
  message += "nMethod: ";
  message += (server.method() == HTTP_GET)?"GET":"POST";
  message += "nArguments: ";
  message += server.args();
  message += "n";
  for (uint8_t i=0; i<server.args(); i++){
    message += " " + server.argName(i) + ": " + server.arg(i) + "n";
  }
  server.send(404, "text/plain", message);
}

/**
 * Service handler for '/api/device/led/toggle'
 * 
 * Toggles the state of the LED are returns a JSON response as {'status': 'true/false'}
 */
void handleLedToggle() 
{
  const char *uri = "/api/device/led/toggle";
  Serial.print("[HTTP][Request] GET on ");
  Serial.println(uri);

  /* Toggle the global state and then write to the LED pin */
  LED_STATE = !LED_STATE;
  digitalWrite(led, LED_STATE);
  Serial.print("LED state is now ");
  Serial.println(LED_STATE);

  server.send(200, "application/json", "{\"success\": true}");
  Serial.print("[HTTP][Response] GET on ");
  Serial.print(uri);
  Serial.println(": 200");
}

/**
 * Setup function pointers for various service handlers for all supported URLs
 */
void registerHTTPServiceHandlers()
{
  server.on("/", handleRoot);
  server.on("/api/device/led/toggle", handleLedToggle); 
  server.onNotFound(handleNotFound);
}

/**
 * Connect to a WiFi AP and print the DHCP-assigned IP address for this device
 */
void connectToWifi()
{
  Serial.print("[WiFi] Connecting to SSID ");
  Serial.print(ssid);
  WiFi.begin(ssid, password);
  /* Wait until the connection is complete */
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("[WiFi] Connected to '");
  Serial.print(ssid);
  Serial.print("' with IP address: ");
  Serial.println(WiFi.localIP());

  /* Register this device on mDNS */ 
  if (MDNS.begin(mDNS_name)) {
    Serial.print("[WiFi] mDNS responder registered for domain name: ");
    Serial.println(mDNS_name);
  } else {
    Serial.print("[WiFi] Failed to register mDNS responder for domain name: ");
    Serial.println(mDNS_name);
  }
}

/**
 * One-time bootstrap
 */
void setup(void)
{
  pinMode(led, OUTPUT);
  digitalWrite(led, 1);
  Serial.begin(115200);
  Serial.println("");

  connectToWifi();
  
  /* Start the HTTP server */
  registerHTTPServiceHandlers();
  server.begin();
  Serial.println("[HTTP] server started");
}

/**
 * Main loop
 */
void loop(void){
  server.handleClient();
}
