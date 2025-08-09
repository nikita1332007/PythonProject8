import requests, json, re

class HeadHunterAPI:
    API="https://api.hh.ru/vacancies"
    def get_vacancies(self, query, pages=1):
        items=[]
        for p in range(pages):
            r=requests.get(self.API, params={"text":query,"page":p})
            r.raise_for_status()
            items += r.json().get("items",[])
        return items

class Vacancy:
    def __init__(self, title, url, salary_text="", description=""):
        self._title=title; self._url=url; self._salary_text=salary_text; self._description=description
        self._avg_salary=self._parse_avg(salary_text)
    @staticmethod
    def _parse_avg(text):
        nums = re.findall(r"\d+", str(text).replace(" ",""))
        if len(nums)>=2: return (int(nums[0])+int(nums[1]))/2
        if len(nums)==1: return int(nums[0])
        return 0
    @classmethod
    def cast_to_object_list(cls, json_list):
        res=[]
        for it in json_list:
            s=it.get("salary") or {}
            salary = ""
            if s: salary = "{}-{} {}".format(s.get("from") or "", s.get("to") or "", s.get("currency") or "")
            res.append(cls(it.get("name",""), it.get("alternate_url",""), salary, (it.get("snippet") or {}).get("requirement","")))
        return res
    def to_dict(self): return {"title":self._title,"url":self._url,"salary":self._salary_text,"description":self._description,"avg":self._avg_salary}
    def __lt__(self, other): return self._avg_salary < other._avg_salary

class JSONSaver:
    def __init__(self,path="vacancies.json"): self.path=path
    def _load(self):
        try: return json.load(open(self.path,encoding="utf-8"))
        except: return []
    def _save(self,data): json.dump(data, open(self.path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    def add_vacancy(self, vac):
        data=self._load()
        if isinstance(vac, list): data += [v.to_dict() for v in vac]
        else: data.append(vac.to_dict())
        self._save(data)
    def delete_vacancy(self, vac):
        data=[d for d in self._load() if d.get("url")!=vac._url]
        self._save(data)

def filter_vacancies(vac_list, keywords):
    return [v for v in vac_list
            if any(kw.lower() in ((v._title or "") + (v._description or "")).lower()
                   for kw in keywords)]

def get_vacancies_by_salary(vac_list, salary_range):
    parts = re.findall(r"\d+", salary_range)
    if not parts: return vac_list
    lo = int(parts[0]); hi = int(parts[1]) if len(parts)>1 else 10**12
    return [v for v in vac_list if lo<=v._avg_salary<=hi]

def sort_vacancies(vac_list): return sorted(vac_list, reverse=True)
def get_top_vacancies(vac_list,n): return vac_list[:n]
def print_vacancies(vac_list):
    for v in vac_list: print(v._title, v._avg_salary, v._url)

def user_interaction():
    hh_api = HeadHunterAPI()
    q=input("Введите поисковый запрос: ")
    pages=int(input("pages: ") or "1")
    raw = hh_api.get_vacancies(q,pages)
    vacancies_list = Vacancy.cast_to_object_list(raw)
    top_n=int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (напр. 100000-150000): ")
    filtered = filter_vacancies(vacancies_list, filter_words) if filter_words!=[''] else vacancies_list
    ranged = get_vacancies_by_salary(filtered, salary_range)
    sorted_v = sort_vacancies(ranged)
    print_vacancies(get_top_vacancies(sorted_v, top_n))

if __name__=="__main__": user_interaction()