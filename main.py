from config import config
from src.head_hunter_api import HeadHunterApi
from src.utils import create_database, save_data_to_database


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем. В функции проверяются следующие возможности: ."""

    params = config()

    # Список компаний для HeadHunter
    vacancy_companies = [
        {"company_id": "5451960", "company_name": "ООО ВФМ Технолоджи"},
        {"company_id": "9943617", "company_name": "ООО Сити Логистик"},
        {"company_id": "5441784", "company_name": "ООО Томикс"},
        {"company_id": "1362151", "company_name": "Герцен"},
        {"company_id": "1651", "company_name": "ООО ТОКК, Завод упаковочных изделий"},
        {"company_id": "1867006", "company_name": "ООО Гравион"},
    ]

    # Создание базы данных vacancies с таблицами companies, vacancies
    create_database("vacancies", params)

    for company in vacancy_companies:
        # Создание экземпляра класса для выгрузки вакансий
        hh_api = HeadHunterApi()
        # Получение вакансий по заданной компании
        company_id = company["company_id"]
        company_name = company["company_name"]
        hh_vacancies = hh_api.get_vacancies(company_id, 5)
        # Добавление данных в базу данных vacancies
        save_data_to_database(hh_vacancies, company_name, "vacancies", params)


if __name__ == "__main__":
    user_interaction()
