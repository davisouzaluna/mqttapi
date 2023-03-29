#!/bin/bash

# Verifica se o pacote pip está instalado
if ! command -v pip &> /dev/null
then
    echo "pip não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install python-pip -y
fi

# Verifica se o pacote paho-mqtt está instalado
if ! python -c "import paho.mqtt.client" &> /dev/null
then
    echo "paho-mqtt não está instalado. Instalando..."
    sudo pip install paho-mqtt
fi

# Verifica se o pacote mosquitto está instalado
if ! command -v mosquitto &> /dev/null
then
    echo "mosquitto não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install mosquitto -y
fi

# Verifica se o pacote mosquitto-clients está instalado
if ! command -v mosquitto_sub &> /dev/null
then
    echo "mosquitto-clients não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install mosquitto-clients -y
fi

# Inicia o broker Mosquitto
sudo service mosquitto start
