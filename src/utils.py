import psycopg2


def create_database(database_name, params):
    """Функция создаёт базу данных и таблицы"""

    conn = None  # без этой строки ошибка, надо спросить почему
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
                    """, (emp['id'], emp['name'], emp['area']['name'], emp['alternate_url'],
                          emp['open_vacancies']))

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
                salary = vac['salary']['from'] if vac['salary'] and vac['salary']['from'] is not None else None
                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                    """, (vac['id'], vac['name'], vac['area']['name'], salary, vac['employer']['id'],
                          vac['alternate_url']))

        conn.commit()

    except Exception as e:
        print(f"Ошибка при сохранении данных вакансий: {e}")

    finally:
        conn.close()
