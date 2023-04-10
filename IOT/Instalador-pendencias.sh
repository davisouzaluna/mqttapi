#!/bin/bash

#instalador de pendências para a utilização correta 
#do programa

#Precisamos do: Mosquitto, mosquitto-clients, pip(para a partir dele instalarmos o paho-mqtt)
#E após tudo isso iniciarmos o broker.


# Verifica se o pacote pip está instalado
if ! command -v pip &> /dev/null # Esse comando descarta a saída padrão(true). Ou seja, caso seja false, não irá ser imprimido nada na tela, já que a saída padrão é a função do dado comando
then
    echo "pip não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install python3-pip -y
fi

# Verifica se o pacote paho-mqtt está instalado
if ! python3 -c "import paho.mqtt.client" &> /dev/null # Esse comando descarta a saída padrão(true). Ou seja, caso seja false, não irá ser imprimido nada na tela, já que a saída padrão é a função do dado comando
then
    echo "paho-mqtt não está instalado. Instalando..."
    sudo pip install paho-mqtt
fi

# Verifica se o pacote mosquitto está instalado
if ! command -v mosquitto &> /dev/null # Esse comando descarta a saída padrão(true). Ou seja, caso seja false, não irá ser imprimido nada na tela, já que a saída padrão é a função do dado comando
then
    echo "mosquitto não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install mosquitto -y
fi

# Verifica se o pacote mosquitto-clients está instalado
if ! command -v mosquitto_sub &> /dev/null # Esse comando descarta a saída padrão(true). Ou seja, caso seja false, não irá ser imprimido nada na tela, já que a saída padrão é a função do dado comando
then
    echo "mosquitto-clients não está instalado. Instalando..."
    sudo apt-get update
    sudo apt-get install mosquitto-clients -y
fi
#verifica se o pymysql tá instalado
if ! dpkg -s python3-pymysql >/dev/null 2>&1; then
    echo "O pacote pymysql não está instalado. Instalando..."
    sudo apt-get update
    pip install pymysql -y # instala o pymysql

fi
# Inicia o broker Mosquitto
sudo service mosquitto start
