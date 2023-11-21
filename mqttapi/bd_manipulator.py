import mysql.connector
import datetime

class MySQLManipulator:
    def __init__(self, host='localhost', user='root', password='', database=None, port=3306, lectures='leituras'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.lectures = lectures
        self.connection = None
        self.cursor = None

    def create_table(self, table=None, lectures=False):
        if table is None:
            table = 'Dispositivo'
        
        
        ###############To create the table of lectures################
        if lectures is True:  
             
            create_table_query_lectures = f"""
                CREATE TABLE IF NOT EXISTS {self.lectures} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_id VARCHAR(255),
                    current_value FLOAT,
                    created_at DATETIME,
                    FOREIGN KEY (sensor_id) REFERENCES {table}(topic)
                        )
                
            """
            
            create_table_query_without_lectures = f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    topic VARCHAR(255) UNIQUE,
                    qos INT
                    )
            
            """
            
            self.cursor.execute(create_table_query_without_lectures)
            self.cursor.execute(create_table_query_lectures)
        ##############################################################
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message VARCHAR(255),
            topic VARCHAR(255),
            qos INT,
            created_at DATETIME
                )
            """
        self.cursor.execute(create_table_query)

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

        if self.database is not None:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.connection.database = self.database

        

    def disconnect(self):
        if self.connection and self.cursor:
            self.cursor.close()
            self.connection.close()

    def insert_data_with_table_lectures(self, sensor_topic, current_value, data_hora_medicao=None, tabela=None, qos=0):
        tabela = tabela or 'sensor'
        
        self.create_table(tabela, lectures=True)

    # Verifica se o dispositivo já existe na tabela
        check_device_query = f"SELECT id FROM {tabela} WHERE topic = %s LIMIT 1"
        self.cursor.execute(check_device_query, (sensor_topic,))
        result = self.cursor.fetchone()

        if not result:
        # O dispositivo não existe, então precisamos inseri-lo antes de adicionar à tabela de leituras
            insert_device_query = f"INSERT INTO {tabela}(topic, qos) VALUES(%s, %s)"
            self.cursor.execute(insert_device_query, (sensor_topic, qos))
            self.connection.commit()

    # Agora podemos inserir os dados na tabela de leituras
        if data_hora_medicao is None:
            data_hora_medicao = datetime.datetime.now(datetime.timezone.utc)

        try:
            insert_query_lectures = f"INSERT INTO {self.lectures}(sensor_id, current_value, created_at) VALUES(%s, %s, %s)"
            self.cursor.execute(insert_query_lectures, (sensor_topic, current_value, data_hora_medicao))
            self.connection.commit()
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            self.connection.rollback()

    def insert_data(self, mensagem, topico, qos, data_hora_medicao=None, tabela=None):
        tabela = tabela or 'Dispositivo'  # Define 'Dispositivo' as the default table if tabela is None

        self.create_table(tabela)
        if data_hora_medicao is None:
            data_hora_medicao = datetime.datetime.now(datetime.timezone.utc)
        
        try:
            insert_query = f"INSERT INTO {tabela}(message, topic, qos, created_at) VALUES(%s, %s, %s, %s)"
            self.cursor.execute(insert_query, (mensagem, topico, qos, data_hora_medicao))
            self.connection.commit()
            
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            self.connection.rollback()
