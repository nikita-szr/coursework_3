import psycopg2


def create_database(database_name: str, params: dict):
    """Функция создаёт базу данных и таблицу"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE employers (
        employer_id INTEGER,
        employer_name TEXT NOT NULL,
        employer_area TEXT NOT NULL,
        url TEXT,
        open_vacancies INTEGER
        )""")