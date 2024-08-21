import psycopg2


def create_database(database_name: str, params: dict):
    """Функция создаёт базу данных и таблицы"""

    conn = None
    try:
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
            cur.execute(f'CREATE DATABASE {database_name}')

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

        with conn.cursor() as cur:
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
