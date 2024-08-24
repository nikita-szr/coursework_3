import requests


def get_employee_data(employer_ids):
    """Функция для получения данных о компаниях с сайта HH.ru"""
    employers = []
    for employer_id in employer_ids:
        url = f"https://api.hh.ru/employers/{employer_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            employer_info = response.json()
            employers.append(employer_info)
        except requests.RequestException as e:
            print(f"Ошибка при запросе данных о компании {employer_id}: {e}")
    return employers


def get_vacancies_data(employer_ids):
    """Функция для получения данных о вакансиях с сайта HH.ru"""
    vacancies = []
    for employer_id in employer_ids:
        url_vacancies = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
        try:
            response = requests.get(url_vacancies, params={'page': 0, 'per_page': 100})
            response.raise_for_status()
            vacancy_info = response.json()
            vacancies.extend(vacancy_info['items'])
        except requests.RequestException as e:
            print(f"Ошибка при запросе данных о вакансиях для компании {employer_id}: {e}")
    return vacancies


employer_ids_list = [9694561, 4219, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]
