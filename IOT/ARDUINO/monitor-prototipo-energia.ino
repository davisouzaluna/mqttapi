#include <ESP8266WiFi.h>//biblioteca do Esp8266(Node MCU)
#include <PubSubClient.h>//biblioteca do mosquitto
#include <EmonLib.h>//biblioteca do sensor de energia
//include "EmonLib.h"  -->caso a linha acima dê errado


//===============================*sensor_de_corrente_com_a_biblioteca_emonlib*================================//
const unsigned int* V_input_pin=2; //utilizei o sinal * pois acho que é uma constante
const double* V_calibration=234.26;
const double* V_phase_shift=1.7;//Obs: o V no começo significa voltagem(da função voltage do emonlib)
const unsigned int* C_input_pin=1;
const double* C_calibration=111.1;//Obs: O C no começo significa current(da função current do emonlib)

//==============================*Wifi*=========================================================================//
const char* ssid = "12345678";//nome da rede
const char* password = "12345678";//senha da rede

//============================*Mosquitto*======================================================================//
const char* mqttServer = "mqtt3.thingspeak.com ";//broker--Recomenda-se alterar para test.mosquitto.org
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const char* topico = "energia_braba";//tópico

//===========================*Variável do payload-mosquitto*===================================================//

//===========================*instancias das classes*==========================================================//
EnergyMonitor monitor;
WiFiClienr espClient;//alterei a variável "WifiClienr" para "WifiClient"
PubSubClient client(espClient);

//===========================*variáveis e outras funções*======================================================//
//bool mqttstatus = 0;
//bool connectMQTT();
//void callback(char *topic,byte *payload,unsigned int length);
//Referencia dessas variáveis: https://github.com/davifurao/Sistema-distribuido/blob/main/arduino_comunicacao_.ino
//seriam utilizadas para verificação de conexão




void setup() {
    Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  client.setServer(mqttServer, mqttPort);
  while (!client.connect("NodeMCU", mqttUser, mqttPassword)) {
    Serial.println("Connecting to MQTT...");
    delay(500);
  }
  Serial.println("Connected to MQTT");
  monitor.voltage(V_input_pin,V_calibration,V_phase_shift);//método do monitor de corrente
  monitor.current(C_input_pin,C_calibration);

}

void loop() {
    float realPower=monitor.realPower();
    char message[1000];
    sprintf(message,"%f",realPower);
    client.publish(topico,message);
    delay(1000);
}
