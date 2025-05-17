from abc import ABC, abstractmethod
from typing import Any


class BaseApi(ABC):
    """Абстрактный класс BaseApi. В нем реализованы класс-методы для подключения и получения данных по
    API-запросу."""

    @abstractmethod
    def api_connect(self) -> dict[Any, Any]:
        """Абстрактный метод для подключения по API."""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> dict[Any, Any]:
        """Абстрактный метод для получения вакансий."""
        pass
