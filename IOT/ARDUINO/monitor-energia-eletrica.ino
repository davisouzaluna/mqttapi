#include <ESP8266WiFi.h>//biblioteca do esp
#include <PubSubClient.h>//biblioteca do mqtt

const char* ssid = "";//nome da rede
const char* password = "";//senha da rede
const char* mqttServer = "test.mosquitto.org";//broker
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const char* topic = "dddfurao";//tópico

WiFiClient espClient;
PubSubClient client(espClient);

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
}

void loop() {
  int value = analogRead(A0);//Lê o pino A0, caso queira fazer alguma alteração no projeto, é só mudar o pino(pino de leitura dos dados)
  char message[1000];
  sprintf(message, "%d", value);
  client.publish(topic, message);//publica a mensagem
  delay(1000);//intervalo entre as mensagens
}


//ps: como a placa É o node MCU, é preciso instalar a placa através
//do link : http://arduino.esp8266.com/stable/package_esp8266com_index.json 
//um tutorial para download da mesma: https://www.fvml.com.br/2018/12/instalando-biblioteca-do-modulo-esp8266.html


//No meu caso foi conectado a placa na entrada usb, então atualiza essa opção quando for configurar a porta
//a placa é o nodeMCU 1.0

//precisa-se também instalar a biblioteca PubSubClient. No meu caso, eu pesquisei
//PubSubClient e instalei a do autor Cloud4RPi , que por conseguinte, instalou as dependências