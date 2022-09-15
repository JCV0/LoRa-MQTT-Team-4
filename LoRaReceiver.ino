#include <LoRa.h> //header file que permite trabajar con dispositivos LoRa
#include "boards.h" //header file para configurar dispositivo
#include <ArduinoJson.hpp> //libreria para trabajar con json
#include <ArduinoJson.h>  
String json; //representa mensaje recibido, en un principio es un string pero como trae formato de json se puede convertir a json

void setup()
{
    //inicializar dispositivo
    initBoard();
    // When the power is turned on, a delay is required.
    delay(1500);

    Serial.println("LoRa Receiver");

    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DI0_PIN);
    if (!LoRa.begin(LoRa_frequency)) {
        Serial.println("Starting LoRa failed!");
        while (1);
    }
    
}

void loop()
{
    // try to parse packet
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
        // se recibio un paquete de datos

        String recv = ""; //mensaje reibido es un string (en formato json)
        // read packet
        while (LoRa.available()) {
            recv += (char)LoRa.read(); //guardar mensaje recibido en variable recv
        }

        StaticJsonDocument<400> doc; //crea objeto que permite codificar mensaje recibido (string) a json

        //si se desea cnvertir de string a json en se descomentan las siguientes lineas de codigo
        //en nuestro caso la conversion de string a json se hace con un programa de python
        //DeserializationError error = deserializeJson(doc,recv);
        //if (error) {
          //Serial.println("error");
          //return;}

        //if (doc["id"] != 4){
          //  Serial.print("mensaje no es de equipo 4");
          //} else {
           // Serial.print(recv);
            
            //}
        

        Serial.println(recv); //enviar mensaje recibido por counicacion serial a programa de python

//las siguientes lineas solo son utiles si se cuenta con un display
#ifdef HAS_DISPLAY
        if (u8g2) {
            u8g2->clearBuffer();
            char buf[256];
            u8g2->drawStr(0, 12, "Received OK!");
            u8g2->drawStr(0, 26, recv.c_str());
            snprintf(buf, sizeof(buf), "RSSI:%i", LoRa.packetRssi());
            u8g2->drawStr(0, 40, buf);
            snprintf(buf, sizeof(buf), "SNR:%.1f", LoRa.packetSnr());
            u8g2->drawStr(0, 56, buf);
            u8g2->sendBuffer();
        }
#endif
    }
}
