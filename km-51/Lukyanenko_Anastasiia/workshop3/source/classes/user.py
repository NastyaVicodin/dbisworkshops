
from flask import Flask
import cx_Oracle


class User:
    id_code = db.Column('id_code', db.NUMERIC, primary_key=True)
    last_name = db.Column('last_name', db.VARCHAR(30))
    first_name = db.Column('first_name', db.VARCHAR(30))
    middle_name = db.Column('middle_name', db.VARCHAR(30))
    login = db.Column('login', db.VARCHAR(30))
    password = db.Column('password', db.VARCHAR(30))
    email = db.Column('email', db.VARCHAR(30))
    salary = db.Column('salary', db.VARCHAR(30))
    specialization = db.Column('specialization', db.VARCHAR(30))
    location = db.Column('location', db.VARCHAR(30))
    sphere = db.Column('sphere', db.VARCHAR(30))

    def __init__(self, login):
        self.id_code = id_code
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.login = login
        self.password = password
        self.salary = salary
        self.specialization = specialization
        self.location = location
        self.sphere = sphere

    def __enter__(self):
        self.__db = cx_Oracle.connect("system", "100498", "127.0.0.1")
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__db.close()

