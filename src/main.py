from utils import create_database, save_data_to_database_emp, save_data_to_database_vac
from config import config
from DBManager import DBManager
from api_hh import get_employee_data, get_vacancies_data, employer_ids_list


def main():
    params = config()
    database_name = 'hh'

    data_emp = get_employee_data(employer_ids_list)
    data_vac = get_vacancies_data(employer_ids_list)
    create_database(database_name, params)
    save_data_to_database_emp(data_emp, database_name, params)
    save_data_to_database_vac(data_vac, database_name, params)

    db_manager = DBManager(params)

    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержится запрашиваемое слово\n"
          f"0 - Выход из программы")

    while True:
        user_input = input('Введите номер запроса\n')
        if user_input == "1":
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании: {companies_and_vacancies_count}\n")

        elif user_input == "2":
            all_vacancies = db_manager.get_all_vacancies()
            print(
                f"Cписок всех вакансий с указанием названия компании, названия вакансии и "
                f"зарплаты и ссылки на вакансию: {all_vacancies}\n")

        elif user_input == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}\n")

        elif user_input == "4":
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(
                f"Список всех вакансий, у которых зарплата выше средней по всем вакансиям: "
                f"{vacancies_with_higher_salary}\n")

        elif user_input == "5":
            keyword = input('Введите ключевое слово ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово: {vacancies_with_keyword}")

        elif user_input == '0':
            break

    db_manager.close()


if __name__ == '__main__':
    main()
