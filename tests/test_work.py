import unittest, tempfile, os, json

from src import work


def make_vac(title, url, salary_text="", description=""):
    v = work.Vacancy.__new__(work.Vacancy)
    v._title = title; v._url = url; v._salary_text = salary_text; v._description = description
    v._avg_salary = work.Vacancy._parse_avg(salary_text)
    return v

class TestWork(unittest.TestCase):
    def test_parse_avg(self):
        self.assertEqual(work.Vacancy._parse_avg("100000-200000"),150000)
        self.assertEqual(work.Vacancy._parse_avg("50000"),50000)
        self.assertEqual(work.Vacancy._parse_avg(""),0)

    def test_filter_handles_none_description(self):
        v = make_vac("Title","http://u","","")
        v._description = None
        res = work.filter_vacancies([v], ["title"])
        self.assertEqual(res, [v])

    def test_jsonsaver_add_delete(self):
        s = work.JSONSaver.__new__(work.JSONSaver)
        s.path = os.path.join(tempfile.gettempdir(),"t_vac.json")
        try:
            if os.path.exists(s.path): os.remove(s.path)
            v = make_vac("T","U","100-200","D")
            s.add_vacancy(v)
            data = json.load(open(s.path, encoding="utf-8"))
            self.assertTrue(any(d.get("url")=="U" for d in data))
            s.delete_vacancy(v)
            data = json.load(open(s.path, encoding="utf-8"))
            self.assertFalse(any(d.get("url")=="U" for d in data))
        finally:
            if os.path.exists(s.path): os.remove(s.path)

    def test_hhapi_get_vacancies_pages(self):
        def fake_get(url, params):
            class R:
                def raise_for_status(self): pass
                def json(self): return {"items":[params["page"]]}
            return R()
        import requests
        orig = requests.get; requests.get = fake_get
        try:
            hh = work.HeadHunterAPI()
            items = hh.get_vacancies("q", pages=3)
            self.assertEqual(len(items), 3)
        finally:
            requests.get = orig

if __name__ == "__main__":
    unittest.main()