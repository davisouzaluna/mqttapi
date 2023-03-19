#!/bin/bash
saida_instrucao = "Caso você queira terminar a operação, aperte Ctrl+c"
function atualizacao(){
sudo apt-get update
sudo apt-get upgrade
sudo apt install mosquitto -y
sudo apt install mosquitto-clients -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
pip install paho-mqtt -y
sudo apt-get update
sudo apt-get upgrade
sudo service mosquitto start

}

atualizacao