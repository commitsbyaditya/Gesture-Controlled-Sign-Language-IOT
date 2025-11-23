/*
 * LCD I2C Display for Sign Language Detection
 * 
 * This Arduino sketch receives sign language predictions via serial
 * and displays them on a 16x2 LCD I2C display.
 * 
 * Hardware Required:
 * - Arduino (Uno, Nano, Mega, etc.)
 * - 16x2 LCD with I2C module
 * 
 * Connections:
 * - LCD SDA -> Arduino A4 (or SDA pin)
 * - LCD SCL -> Arduino A5 (or SCL pin)
 * - LCD VCC -> Arduino 5V
 * - LCD GND -> Arduino GND
 * 
 * Serial Commands:
 * - "TEXT:your_text" - Display text on LCD
 * - "CLEAR" - Clear the LCD display
 * 
 * Author: Integrated Hand Gesture System
 * Date: 2025
 */

 #include <Wire.h>
 #include <LiquidCrystal_I2C.h>
 
 // LCD Configuration
 // Set the LCD address to 0x27 for a 16 chars and 2 line display
 // Common addresses are 0x27 or 0x3F - try both if display doesn't work
 LiquidCrystal_I2C lcd(0x27, 16, 2);
 
 // Variables
 String inputString = "";
 boolean stringComplete = false;
 
 void setup() {
   // Initialize serial communication
   Serial.begin(9600);
   
   // Initialize LCD
   lcd.init();
   lcd.backlight();
   
   // Display welcome message
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print("Sign Language");
   lcd.setCursor(0, 1);
   lcd.print("Detector Ready!");
   
   delay(2000);
   lcd.clear();
   lcd.setCursor(0, 0);
   lcd.print("Waiting...");
   
   // Reserve memory for input string
   inputString.reserve(200);
   
   Serial.println("LCD Display Ready");
 }
 
 void loop() {
   // Check for serial data
   if (stringComplete) {
     processCommand(inputString);
     inputString = "";
     stringComplete = false;
   }
 }
 
 // Serial event handler
 void serialEvent() {
   while (Serial.available()) {
     char inChar = (char)Serial.read();
     
     if (inChar == '\n') {
       stringComplete = true;
     } else {
       inputString += inChar;
     }
   }
 }
 
 // Process incoming commands
 void processCommand(String command) {
   command.trim();
   
   if (command.startsWith("TEXT:")) {
     // Extract text after "TEXT:"
     String text = command.substring(5);
     displayText(text);
   }
   else if (command == "CLEAR") {
     lcd.clear();
     lcd.setCursor(0, 0);
     lcd.print("Waiting...");
     Serial.println("LCD Cleared");
   }
   else {
     Serial.println("Unknown command: " + command);
   }
 }
 
 // Display text on LCD
 void displayText(String text) {
   lcd.clear();
   
   // Line 1: Label
   lcd.setCursor(0, 0);
   lcd.print("Sign:");
   
   // Line 2: The detected sign
   lcd.setCursor(0, 1);
   
   // Truncate if text is too long for 16 characters
   if (text.length() > 16) {
     text = text.substring(0, 16);
   }
   
   // Center the text if it's short
   int padding = (16 - text.length()) / 2;
   lcd.setCursor(padding, 1);
   lcd.print(text);
   
   Serial.println("Displayed: " + text);
 }
 
 /*
  * Troubleshooting:
  * 
  * 1. If LCD shows nothing:
  *    - Check I2C address (try 0x3F instead of 0x27)
  *    - Verify connections (SDA, SCL, VCC, GND)
  *    - Adjust LCD contrast potentiometer
  * 
  * 2. To find I2C address, use I2C Scanner sketch:
  *    File -> Examples -> Wire -> i2c_scanner
  * 
  * 3. If characters are garbled:
  *    - Check baudrate matches (9600)
  *    - Ensure proper serial termination (\n)
  * 
  * 4. Required Libraries:
  *    - LiquidCrystal_I2C by Frank de Brabander
  *    - Install via: Sketch -> Include Library -> Manage Libraries
  */
 