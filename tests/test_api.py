import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import unittest
import tempfile
from unittest.mock import patch, MagicMock

from src import vacancy, main, interactions


class TestVacancy(unittest.TestCase):
    def test_vacancy_basic(self):
        v = vacancy.Vacancy("T", "u", 10, 20, "RUB", "req")
        self.assertEqual(v._title, "T")
        self.assertEqual(v._currency, "RUB")
        self.assertEqual(v._avg, 15)
        d = v.to_dict()
        self.assertIn('title', d)
        self.assertIn('avg', d)

class TestMainIntegration(unittest.TestCase):
    def test_run_integration_mocks(self):
        raw = [
            {'name':'A','alternate_url':'urlA','salary':{'from':100,'to':200,'currency':'USD'}, 'snippet':{'requirement':'rA'}},
            {'name':'B','alternate_url':'urlB','salary':{'from':50,'to':70,'currency':'EUR'}, 'snippet':{'requirement':'rB'}}
        ]
        class FakeAPI:
            def get_vacancies(self, *a, **k): return raw

        # use real Vacancy but ensure behavior deterministic
        class FakeStorage:
            def __init__(self): self.added=None
            def add(self, lst): self.added=lst

        with patch.object(main, 'HHAPI', FakeAPI), \
             patch.object(main, 'JSONStorage', FakeStorage), \
             patch('builtins.print') as mock_print:
            main.run()
            self.assertEqual(mock_print.call_count, 2)

class TestInteractions(unittest.TestCase):
    def test_interact_callable(self):
        self.assertTrue(callable(interactions.interact))

if __name__ == '__main__':
    unittest.main()