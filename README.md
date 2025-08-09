# Курсовая работа

Простой поиск вакансий с HeadHunter и локальным сохранением в JSON

# Требования
- Python 3.7+
- requests

# Установка
shell

pip install requests

# Запуск
Запустить интерактивный режим
shell

python work.py
По умолчанию результат сохраняется в файл vacancies.json

# Запуск тестов
shell

python -m unittest discover -s tests

# Краткое описание API
- HeadHunterAPI.getvacancies(query, pages=1) возвращает список сырых вакансий
- Vacancy.casttoobjectlist(jsonlist) конвертирует в объекты Vacancy
- JSONSaver.addvacancy / deletevacancy управляют файлом JSON
- filtervacancies, getvacanciesbysalary, sortvacancies, gettopvacancies — утилиты фильтрации и сортировки