from api import HHAPI
from vacancy import Vacancy
from storage import JSONStorage
from interactions import interact

def human(vac: Vacancy) -> str:
    return f"{vac._title} — {vac._avg} {vac._currency} ({vac._url})"

def run():
    api = HHAPI()
    raw = api.get_vacancies("python", per_page=20)
    vacs = [Vacancy(it['name'], it['alternate_url'],
                    (it.get('salary') or {}).get('from'),
                    (it.get('salary') or {}).get('to'),
                    (it.get('salary') or {}).get('currency') or "",
                    (it.get('snippet') or {}).get('requirement', "")) for it in raw]
    vacs.sort(reverse=True)
    storage = JSONStorage()
    storage.add([v.to_dict() for v in vacs])
    for v in vacs[:10]:
        print(human(v))

if __name__ == "__main__":
    interact()