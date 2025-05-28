from typing import Any

import psycopg2
from psycopg2 import Error


class DBManager:
    """Класс DBManager для подключения к базе данным и получению данных по разным методам."""

    def __init__(self, params: dict):
        """Метод для инициализации экземпляра класса DBManager."""
        self.conn = psycopg2.connect(dbname="vacancies", **params)
        self.cur = self.conn.cursor()
        self.company_table = "companies"
        self.vacancy_table = "vacancies"
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Метод возвращает список всех компаний и количество вакансий у каждой компании."""
        try:
            with self.conn:
                self.cur.execute(
                    f"""select {self.company_table}.name, count(*)
                from {self.vacancy_table}
                join {self.company_table} using(company_id)
                group by {self.company_table}.name"""
                )
                data = self.cur.fetchall()
                data_dict = [{"Наименование компании": d[0], "Количество вакансий": d[1]} for d in data]
            return data_dict
        except Error as e:
            print(f"Ошибка: {e}")

    def get_all_vacancies(self) -> list[dict]:
        """Метод возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки
        на вакансию."""
        try:
            with self.conn:
                self.cur.execute(
                    f"""select {self.company_table}.name, {self.vacancy_table}.name, salary_from, salary_to, url
                from {self.vacancy_table}
                join {self.company_table} using(company_id)"""
                )
                data = self.cur.fetchall()
                data_dict = [
                    {
                        "Наименование компании": d[0],
                        "Наименование вакансии": d[1],
                        "Зарплата от": d[2],
                        "Зарплата до": d[3],
                        "Ссылка на вакансию": d[4],
                    }
                    for d in data
                ]
            return data_dict
        except Error as e:
            print(f"Ошибка: {e}")

    def get_avg_salary(self) -> Any:
        """Метод возвращает среднюю зарплату по всем вакансиям."""
        try:
            with self.conn:
                self.cur.execute(
                    f"""select avg(salary_from + salary_to)
                    from {self.vacancy_table}"""
                )
                data = self.cur.fetchall()
                for d in data:
                    return f"Средняя зарплата: {round(d[0], 2)}"
        except Error as e:
            print(f"Ошибка: {e}")

    def get_vacancies_with_higher_salary(self, avg_value: float = 0) -> list[dict]:
        """Метод возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            with self.conn:
                self.cur.execute(
                    f"""select name, url
                    from {self.vacancy_table}
                    where (salary_from + salary_to) / 2 > {avg_value}"""
                )
                data = self.cur.fetchall()
                data_dict = [{"Вакансия": d[0], "Ссылка на вакансию": d[1]} for d in data]
            return data_dict
        except Error as e:
            print(f"Ошибка: {e}")

    def get_vacancies_with_keyword(self, keyword: list) -> list[dict]:
        """Метод возвращает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        try:
            with self.conn:
                and_like = "and name like %s " * (len(keyword) - 1)
                self.cur.execute(
                    f"""select name, url
                    from {self.vacancy_table}
                    where name like %s {and_like}""",
                    tuple(
                        [f"%{word}%" for word in keyword],
                    ),
                )
                data = self.cur.fetchall()
                data_dict = [{"Вакансия": d[0], "Ссылка на вакансию": d[1]} for d in data]
                return data_dict
        except Error as e:
            print(f"Ошибка: {e}")
