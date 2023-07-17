import mysql.connector
import datetime

class MySQLManipulator:
    def __init__(self, host='localhost', user='root', password='', database=None, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

    def create_table(self, table=None):
        if table is None:
            table = 'Dispositivo'

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

    def insert_data(self, mensagem, topico, qos, data_hora_medicao=None, tabela=None):
        tabela = tabela or 'Dispositivo'  # Define 'Dispositivo' as the default table if tabela is None

        self.create_table(tabela)
        if data_hora_medicao is None:
            data_hora_medicao = datetime.datetime.now(datetime.timezone.utc)
        insert_query = f"INSERT INTO {tabela}(message, topic, qos, created_at) VALUES(%s, %s, %s, %s)"
        self.cursor.execute(insert_query, (mensagem, topico, qos, data_hora_medicao))
        self.connection.commit()
