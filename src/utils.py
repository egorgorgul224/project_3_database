import psycopg2


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения компаний и вакансий."""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
                )
            """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(company_id),
                head_hunter_id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                experience TEXT
                )
            """
        )

    conn.commit()
    conn.close()


def save_data_to_database(vacancy_data: list[dict], company: str, database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO companies (name)
            VALUES (%s)
            RETURNING company_id
            """,
            (company,),
        )
        company_id = cur.fetchone()[0]
        for vacancy in vacancy_data:
            salary_info = vacancy.get("salary", {})
            if salary_info:
                salary_from = salary_info.get("from", 0)
                salary_to = salary_info.get("to", 0)
            else:
                salary_from = 0
                salary_to = 0
            vacancy_experience_name = vacancy.get("experience", {}).get("name", "")
            cur.execute(
                """
                INSERT INTO vacancies (company_id, head_hunter_id, name, url, salary_from, salary_to, experience)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    company_id,
                    vacancy["id"],
                    vacancy["name"],
                    vacancy["alternate_url"],
                    salary_from,
                    salary_to,
                    vacancy_experience_name,
                ),
            )

    conn.commit()
    conn.close()
