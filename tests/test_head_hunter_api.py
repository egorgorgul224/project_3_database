from unittest.mock import MagicMock, patch

import pytest

from src.head_hunter_api import HeadHunterApi


def test_category_init(head_hunter_init: HeadHunterApi) -> None:
    """Тест проверяет корректное создания экземпляра класса HeadHunterApi."""
    assert head_hunter_init.url == "https://api.hh.ru/vacancies"
    assert head_hunter_init.headers == {"User-Agent": "HH-User-Agent"}
    assert head_hunter_init.params == {"text": "", "page": 0, "per_page": 10}
    assert head_hunter_init.vacancies == []


@patch("requests.get")
def test_api_connect(mocked_get: MagicMock, api_connect_data: list[dict], head_hunter_init: HeadHunterApi) -> None:
    """Тест проверяет корректный вывод списка json-данных с вакансиями."""

    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = api_connect_data
    result = head_hunter_init.api_connect()
    assert result == [
        {
            "name": "Python Developer",
            "alternate_url": "<https://hh.ru/vacancy/123456>",
            "salary": {"from": 100000, "to": 150000},
            "experience": {"name": "Требования: опыт работы от 3 лет"},
        }
    ]

    mocked_get.assert_called()


@patch("requests.get")
def test_api_connect_status_code_error(
    mocked_get: MagicMock, api_connect_data: list[dict], head_hunter_init: HeadHunterApi
) -> None:
    """Тест проверяет корректный вывод ошибки, если status code не равен 200."""

    mocked_get.return_value.status_code = 404

    with pytest.raises(Exception) as exc_message:
        head_hunter_init.api_connect()

    assert "Ошибка: 404" in str(exc_message)
    mocked_get.assert_called()


@patch("requests.get")
def test_get_vacancies(
    mocked_get: MagicMock, api_connect_data_before_sort: list[dict], head_hunter_init: HeadHunterApi
) -> None:
    """Тест проверяет корректный вывод списка json-данных с вакансиями по ключу."""
    hh = HeadHunterApi()
    keyword = "Python"
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = api_connect_data_before_sort
    result = hh.get_vacancies(keyword)
    assert result == [
        {
            "name": "Python Developer",
            "alternate_url": "<https://hh.ru/vacancy/123456>",
            "salary": {"from": 100000, "to": 150000},
            "experience": {"name": "Требования: опыт работы от 3 лет"},
        },
        {
            "items": {
                "name": "Python Developer",
                "alternate_url": "<https://hh.ru/vacancy/123458>",
                "salary": {"from": 300000, "to": 400000},
                "experience": {"name": "Требования: опыт работы от 5 лет"},
            }
        },
    ]

    mocked_get.assert_called_once()
