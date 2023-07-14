import pymysql

class BDManipulator:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        if self.connection and self.cursor:
            self.cursor.close()
            self.connection.close()

    def insert_data(self, mensagem, topico, qos, data_hora_medicao):
        data_hora_medicao
        insert_query = "INSERT INTO Dispositivo(mensagem, topico, qos, data_hora_medicao) VALUES(%s, %s, %s, %s)"
        self.cursor.execute(insert_query, (mensagem, topico, qos, data_hora_medicao))
        self.connection.commit()
