import cx_Oracle

from dao.dbCredentials import *


class Vacancy:
    def __init__(self):
        self.__db = cx_Oracle.connect(username, password, databaseName)
        self.__cursor = self.__db.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__db.close()

    def get_vacancy(self, p_vacancy_name, p_email):
        query = 'select * from table(vacancy.get_vacancy(:vacancy_name,:email))'
        self.__cursor.execute(query, vacancy_name=p_vacancy_name, email=p_email)
        vacancy = self.__cursor.fetchall()
        return vacancy[0]

    def get_all_vacancies(self):
        query = 'select * from vacancy'
        self.__cursor.execute(query)
        vacancies = self.__cursor.fetchall()
        return vacancies
