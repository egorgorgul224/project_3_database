from typing import Any


class Vacancy:
    """Класс Vacancy для работы с вакансиями."""

    name: str
    url: str
    salary_from: int
    salary_to: int
    experience: str
    __slots__ = ("name", "url", "salary_from", "salary_to", "experience")

    def __init__(self, name: str, url: str, salary_from: int, salary_to: int, experience: str = "") -> None:
        """Метод для инициализации экземпляра класса Vacancy."""

        self.name = self.__verify_str_data(name)
        self.url = self.__verify_str_data(url)
        self.salary_from = self.__verify_int_data(salary_from)
        self.salary_to = self.__verify_int_data(salary_to)
        self.experience = experience

    def __str__(self) -> str:
        """Магический метод для отображения информации об объекте класса."""
        if self.salary_from == 0 and self.salary_to == 0:
            salary_info = "не указана"
        elif self.salary_from == 0:
            salary_info = f"до {self.salary_to}"
        elif self.salary_to == 0:
            salary_info = f"от {self.salary_from}"
        else:
            salary_info = f"от {self.salary_from} до {self.salary_to}"

        if self.experience:
            experience_info = self.experience
        else:
            experience_info = "не указан"

        vacancy_info = f"{self.name}. Ссылка: {self.url}. Зарплата: {salary_info}. Требуемый опыт: {experience_info}."
        return vacancy_info

    @classmethod
    def process_vacancy(cls, vacancy_json_data: dict) -> Any:
        """Классовый метод для обработки информации по вакансии из json-данных и формирования экземпляра класса."""
        name = vacancy_json_data.get("name", "")
        url = vacancy_json_data.get("alternate_url", "")

        salary_info = vacancy_json_data.get("salary", {})
        if salary_info:
            salary_from = salary_info.get("from", 0)
            salary_to = salary_info.get("to", 0)
        else:
            salary_from = 0
            salary_to = 0

        experience_info = vacancy_json_data.get("experience", {})
        if experience_info:
            experience_name = experience_info.get("name", "")
        else:
            experience_name = ""

        return cls(name=name, url=url, salary_from=salary_from, salary_to=salary_to, experience=experience_name)

    @classmethod
    def cast_to_object_list(cls, vacancy_json_data: list[dict]) -> list:
        """Классовый метод для создания списка экземпляров класса из списка словарей."""
        vacancies_list = []
        for vacancy in vacancy_json_data:
            vacancies_list.append(cls.process_vacancy(vacancy))
        return vacancies_list

    def transform_to_dict(self) -> dict:
        """Метод для преобразования экземпляра класса Vacancy в словарь. Используется при добавлении
        экземпляра класса в файл."""
        return {
            "name": self.name,
            "alternate_url": self.url,
            "salary": {"from": self.salary_from, "to": self.salary_to},
            "experience": {"name": self.experience},
        }

    @staticmethod
    def __verify_str_data(check_str_data: str) -> str:
        """Приватный статический метод проверяет валидность строковых данных."""
        if not isinstance(check_str_data, str):
            raise TypeError(f"Атрибут {check_str_data} должен быть строкового типа")
        return check_str_data

    @staticmethod
    def __verify_int_data(check_int_data: int) -> int:
        """Приватный статический метод проверяет валидность целочисленных данных. Метод проверяет, что атрибут является
        экземпляром класса int, не отрицательный."""
        if check_int_data is None:
            return 0
        if not isinstance(check_int_data, int):
            raise TypeError(f"Атрибут {check_int_data} не является числом")
        if check_int_data < 0:
            raise ValueError(f"Атрибут {check_int_data} не может быть ниже 0")
        return check_int_data

    @staticmethod
    def __verify_salary_other(other_data: Any) -> None:
        """Приватный статический метод проверяет валидность зарплаты другого объекта класса Vacancy при
        сравнении зарплат."""
        if not isinstance(other_data, Vacancy):
            raise TypeError("Атрибут не относится к классу Vacancy")
