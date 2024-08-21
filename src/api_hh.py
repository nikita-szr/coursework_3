import requests


def get_employee_data(employer_ids):
    """функция для получения данных о компаниях с сайта HH.ru"""
    employers = []
    for employer_id in employer_ids:
        url = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url, ).json()
        employers.append(employer_info)
    return employers


def get_vacancies_data(employer_ids):
    """функция для получения данных о вакансиях с сайта HH.ru"""
    vacancy = []
    for vacacies_id in employer_ids:
        url_vacancies = f"https://api.hh.ru/vacancies?employer_id={vacacies_id}"
        vacancy_info = requests.get(url_vacancies, params={'page': 0, 'per_page': 100}).json()
        vacancy.extend(vacancy_info['items'])
    return vacancy


# employer_ids_list = [9694561, 4219, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]
