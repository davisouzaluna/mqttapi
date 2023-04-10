create database Reluz_API;
use Reluz_API;


create table monitoramento(
id int not null auto_increment,
topico varchar (255) not null,
mensagem int not null,
qos int not null,
constraint pk_monitoramento primary key (id)
);
