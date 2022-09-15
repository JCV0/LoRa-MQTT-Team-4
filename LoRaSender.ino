//equipo 4
//programa para dispositivo LoRa emisor
//Santiago Ortiz Suzarte A01750402
//Emilio Caudillo Gispert A01750428
//Jorge Antonio Castilla Valdez    A01749166
//Bruno Sánchez García A01378960

#include <LoRa.h>
#include "boards.h"
#include <ArduinoJson.hpp> //libreria para trabajar con datos en formato json
#include <ArduinoJson.h>

int counter = 0;

void setup()
{
    initBoard();//iniciar dispositivo LoRa
    // When the power is turned on, a delay is required.
    delay(1500);

    //configuracion inicial de dispositivo
    Serial.println("LoRa Sender");
    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DI0_PIN);
    if (!LoRa.begin(LoRa_frequency)) {
        Serial.println("Starting LoRa failed!");
        while (1);
    }
}

void loop()
{
    String message; //mensaje que se va a enviar a receptor, contiene datos de sensores
    
    if (Serial.available()) { //determinar si hay bytes disponibles para leer en puerto serial
        message = Serial.readStringUntil('\n'); //leer mensaje que se haya enviado por puerto serial hasta encontrar salto de linea
      
      }

    
    //Serial.print("Sending packet: ");
    //Serial.println(counter);

    // send packet, enivar datos de sensores recibidos por puerto serial a LoRa receptor
    LoRa.beginPacket(); 
    LoRa.print(message); //enviar mensaje
    //LoRa.print(counter);
    LoRa.endPacket(); 
    
//codigo para hacer funcionar display
#ifdef HAS_DISPLAY
    if (u8g2) {
        char buf[256];
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Transmitting: OK!");
        snprintf(buf, sizeof(buf), "Sending: %d", counter);
        u8g2->drawStr(0, 30, buf);
        u8g2->sendBuffer();
    }
#endif
    counter++;
    delay(5000);
}
