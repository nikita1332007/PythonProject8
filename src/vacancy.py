from typing import Optional
class Vacancy:
    __slots__=("_title","_url","_salary_from","_salary_to","_currency","_description","_avg")
    def __init__(self,title:str,url:str,salary_from:Optional[int]=None,salary_to:Optional[int]=None,currency:str="",description:str=""):
        self._title=title; self._url=url
        self._salary_from=self._validate_salary(salary_from); self._salary_to=self._validate_salary(salary_to)
        self._currency=currency; self._description=description; self._avg=self._compute_avg()
    def _validate_salary(self,v:Optional[int]) -> Optional[int]:
        if v is None: return None
        if v<0: raise ValueError("salary must be >=0")
        return int(v)
    def _compute_avg(self) -> float:
        if self._salary_from and self._salary_to: return (self._salary_from+self._salary_to)/2
        return float(self._salary_from or self._salary_to or 0)
    def to_dict(self) -> dict: return {"title":self._title,"url":self._url,"salary_from":self._salary_from,"salary_to":self._salary_to,"currency":self._currency,"description":self._description,"avg":self._avg}
    def __lt__(self, other): return self._avg < other._avg
