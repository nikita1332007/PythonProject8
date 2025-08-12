from abc import ABC, abstractmethod
import requests
from typing import List, Dict

class BaseAPI(ABC):
    """Абстрактный класс для API"""
    def __init__(self, base_url: str): self._base_url = base_url
    def _connect(self, path: str, params: dict) -> requests.Response:
        r = requests.get(f"{self._base_url}{path}", params=params); r.raise_for_status(); return r
    @abstractmethod
    def get_vacancies(self, text: str, per_page:int=20, page:int=0) -> List[Dict]: ...
class HHAPI(BaseAPI):
    def __init__(self): super().__init__("https://api.hh.ru")
    def get_vacancies(self, text: str, per_page:int=20, page:int=0):
        params={"text":text,"per_page":per_page,"page":page}
        return self._connect("/vacancies", params).json().get("items", [])