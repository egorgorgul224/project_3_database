import re

import pandas as pd

from config import config
from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterApi
from src.utils import create_database, save_data_to_database


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем. В функции проверяются следующие возможности: ."""

    params = config()
    exit_value = 1

    # Список компаний для HeadHunter
    vacancy_companies = [
        {"company_id": "5451960", "company_name": "ООО ВФМ Технолоджи"},
        {"company_id": "9943617", "company_name": "ООО Сити Логистик"},
        {"company_id": "5441784", "company_name": "ООО Томикс"},
        {"company_id": "1362151", "company_name": "Герцен"},
        {"company_id": "1651", "company_name": "ООО ТОКК, Завод упаковочных изделий"},
        {"company_id": "1867006", "company_name": "ООО Гравион"},
        {"company_id": "58320", "company_name": "АО Россельхозбанк"},
        {"company_id": "193205", "company_name": "TDM ELECTRIC"},
        {"company_id": "3396763", "company_name": "ООО Премиум Пет"},
        {"company_id": "54378", "company_name": "Карекс-Центр, Группа компаний"},
    ]

    print("Происходит создание базы данных...")
    # Создание базы данных vacancies с таблицами companies, vacancies
    create_database("vacancies", params)

    print("База данных создана. Добавляем компании и вакансии...")
    for company in vacancy_companies:
        # Создание экземпляра класса для выгрузки вакансий
        hh_api = HeadHunterApi()
        company_id = company["company_id"]
        company_name = company["company_name"]
        # Получение вакансий по заданной компании
        hh_vacancies = hh_api.get_vacancies(company_id, 5)
        # Добавление данных в базу данных vacancies
        save_data_to_database(hh_vacancies, company_name, "vacancies", params)

    # Создание экземпляра класса DBManager для получения данных из базы данных vacancies
    db_manager = DBManager(params)

    print("Компании и вакансии созданы.")
    while exit_value == 1:
        menu_item = input(
            """Выберите интересующий пункт:
1. Список компаний и количество вакансий
2. Список всех вакансий
3. Средняя зарплата по всем вакансиям
4. Список вакансий, у которых зарплата выше средней зарплаты
5. Поиск по вакансиям
0. Выйти из приложения
"""
        )

        if menu_item == "1":
            result = pd.DataFrame(db_manager.get_companies_and_vacancies_count())
            print(f"{result}\n")
        elif menu_item == "2":
            result = pd.DataFrame(db_manager.get_all_vacancies())
            print(f"{pd.concat([result.head(5), result.tail(5)])}\n")
        elif menu_item == "3":
            result = db_manager.get_avg_salary()
            print(f"{result}\n")
        elif menu_item == "4":
            result = pd.DataFrame(db_manager.get_vacancies_with_higher_salary())
            print(f"{result}\n")
        elif menu_item == "5":
            word = re.split(r"[,. ]+", input("Введите слово(а) для поиска вакансий: ").lower())
            result = pd.DataFrame(db_manager.get_vacancies_with_keyword(word))
            if result.empty:
                print("По вашему запросу не найдено вакансий")
            else:
                print(f"{result}\n")
        elif menu_item == "0":
            exit_value = 0
            print("Успешный выход")


if __name__ == "__main__":
    user_interaction()
