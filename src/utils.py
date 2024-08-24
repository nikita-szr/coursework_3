import psycopg2
from psycopg2 import sql


def create_database(database_name, params):
    """Функция создаёт базу данных и таблицы"""
    conn = None
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(sql.SQL('DROP DATABASE IF EXISTS {}').format(sql.Identifier(database_name)))
            cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(database_name)))

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name TEXT NOT NULL,
                employer_area TEXT NOT NULL,
                url TEXT,
                open_vacancies INTEGER
            )
            """)

            cur.execute("""
                CREATE TABLE vacancy (
                    vacancy_id INTEGER PRIMARY KEY,
                    vacancy_name TEXT,
                    vacancy_area TEXT,
                    salary INTEGER,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_url TEXT
                )
            """)

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        if conn:
            conn.close()


def save_data_to_database_emp(data_emp, database_name, params) -> None:
    """Функция для заполнения таблицы работодателей в БД"""
    conn = psycopg2.connect(dbname=database_name, **params)
    try:
        with conn.cursor() as cur:
            for emp in data_emp:
                cur.execute("""
                    INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (employer_id) DO NOTHING
                    """, (emp.get('id'), emp.get('name'), emp.get('area', {}).get('name'), emp.get('alternate_url'),
                          emp.get('open_vacancies')))
        conn.commit()

    except Exception as e:
        print(f"Ошибка при сохранении данных работодателей: {e}")

    finally:
        conn.close()


def save_data_to_database_vac(data_vac, database_name, params) -> None:
    """Функция для заполнения таблицы вакансий в БД"""
    conn = psycopg2.connect(dbname=database_name, **params)
    try:
        with conn.cursor() as cur:
            for vac in data_vac:
                salary = vac.get('salary', {}).get('from')
                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                    """, (vac.get('id'), vac.get('name'), vac.get('area', {}).get('name'),
                          salary, vac.get('employer', {}).get('id'),
                          vac.get('alternate_url')))
        conn.commit()

    except Exception as e:
        print(f"Ошибка при сохранении данных вакансий: {e}")

    finally:
        conn.close()
