import pytest

from src.head_hunter_api import HeadHunterApi


@pytest.fixture
def head_hunter_init() -> HeadHunterApi:
    return HeadHunterApi()


@pytest.fixture
def api_connect_data() -> list[dict]:
    return [
        {
            "name": "Python Developer",
            "alternate_url": "<https://hh.ru/vacancy/123456>",
            "salary": {"from": 100000, "to": 150000},
            "experience": {"name": "Требования: опыт работы от 3 лет"},
        }
    ]


@pytest.fixture
def api_connect_data_before_sort() -> dict:
    return {
        "items": [
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
    }
