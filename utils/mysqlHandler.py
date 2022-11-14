import mysql.connector as Client
from utils.constants.config import PORT, MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DEFAULTDB
from tkinter import messagebox

class DBManager:
    def __init__(self):
        self.client = Client.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=DEFAULTDB,
            port = PORT,
            auth_plugin='mysql_native_password'
        )
        self.executor = self.client.cursor()

    def executeCommand(self, command):
        self.executor.execute(command)
        try:
            self.client.commit()
            return self.executor.fetchall()
        except Client.errors.InterfaceError:
            self.client.rollback()
            return -1
        except Client.errors.InternalError:
            return self.executor.fetchall()
