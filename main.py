from src.head_hunter_api import HeadHunterApi
from src.vacancy import Vacancy
from config import config


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем. В функции проверяются следующие возможности: ."""

    params = config()

    # Список компаний для HeadHunter
    vacancy_companies = []

    # Создание экземпляра класса для выгрузки вакансий
    hh_api = HeadHunterApi()

    for company in vacancy_companies:
        hh_vacancies = hh_api.get_vacancies(company, 20)
        # Формирование списка экземпляров класса вакансий из полученных данных
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)


if __name__ == "__main__":
    user_interaction()
