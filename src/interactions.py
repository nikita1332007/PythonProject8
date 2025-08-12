from api import HHAPI
from vacancy import Vacancy
from storage import JSONStorage
from typing import List

def _human(v: Vacancy) -> str:
    return f"{v._title} — {v._avg} {v._currency} ({v._url})"

def interact():
    api = HHAPI()
    storage = JSONStorage()
    while True:
        print("\nМеню\n1 Поиск и сохранить\n2 Показать сохранённые\n3 Удалить по URL\n4 Выход")
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            kw = input("Ключевое слово: ").strip()
            per = int(input("Результатов на страницу (по умолчанию 20): ") or 20)
            raw = api.get_vacancies(kw, per_page=per)
            vacs = [Vacancy(it['name'], it['alternate_url'],
                            (it.get('salary') or {}).get('from'),
                            (it.get('salary') or {}).get('to'),
                            (it.get('salary') or {}).get('currency') or "",
                            (it.get('snippet') or {}).get('requirement',""))
                    for it in raw]
            storage.add([v.to_dict() for v in vacs])
            print(f"Сохранено {len(vacs)} вакансий")
        elif choice == "2":
            data = storage.load()
            vacs = [Vacancy(d['title'], d['url'], d.get('salary_from'), d.get('salary_to'), d.get('currency'), d.get('description')) for d in data]
            vacs.sort(reverse=True)
            for v in vacs[:30]:
                print(_human(v))
        elif choice == "3":
            url = input("URL вакансии для удаления: ").strip()
            storage.remove(url)
            print("Удалено (если было)")
        elif choice == "4":
            print("Выход"); break
        else:
            print("Неверный пункт")
if __name__=="__main__":
    interact()