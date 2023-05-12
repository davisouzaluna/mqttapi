create database ReLUZ_API;
use ReLUZ_API;

CREATE TABLE dispositivos (
  id INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  descricao VARCHAR(255) NOT NULL,
  MAC_FK VARCHAR(12) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (MAC_FK) REFERENCES usuario(id)
);

CREATE TABLE sensor (
  id INT NOT NULL AUTO_INCREMENT,
  MAC VARCHAR(12) NOT NULL,
  corrente FLOAT NOT NULL,
  data_hora_medicao DATETIME NOT NULL,
  qos FLOAT NOT NULL,
  log_erro_id INT,
  PRIMARY KEY (id),
  FOREIGN KEY (log_erro_id) REFERENCES log_erro(id)
);

CREATE TABLE log_erro (
  id INT NOT NULL AUTO_INCREMENT,
  tipo VARCHAR(255) NOT NULL,
  mensagem TEXT NOT NULL,
  data_hora DATETIME NOT NULL,
  PRIMARY KEY (id)
);
