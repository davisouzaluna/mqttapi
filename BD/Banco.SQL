create database ReLUZ;
use ReLUZ;

create table usr_USUARIO(
usr_id int not null auto_increment,
usr_nome varchar(60) not null,
usr_senha varchar(60) not null,
constraint primary key(usr_id)
);

create table iot_dispositivo(
    iot_id int not null auto_increment,
    iot_topico varchar(60),
    iot_usr_fk int not null,
    primary key (iot_id),
    foreign key(iot_usr_fk) references usr_USUARIO(usr_id)
);

create table log_err(
    log_id int not null auto_increment,
    log_horario timestamp default current_timestamp,
    log_data date,
    log_hora time,
    log_iot_fk int not null,
    primary key(log_id),
    foreign key(log_iot_fk) references iot_dispositivo(iot_id)
);
create table messages(
    messages_id not null auto_increment,
    messages_payload varchar(80),
    messages_topico_fk varchar,
    primary key (messages_id),
    foreign key(messages_topico_fk) references iot_dispositivo(iot_id)/*Cada dispositivo vai ter um tópico(por isso que eu apontei para o id do dispositivo)*/
);

