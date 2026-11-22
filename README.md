# API to PostgreSQL ETL Pipeline

ETL-пайплайн с оркестрацией через Apache Airflow.

## Архитектура

Python (extract) → Python (transform/dedup) → PostgreSQL → Airflow (оркестрация)

Все сервисы запускаются через Docker Compose.

## Стек
- Python 3 (requests, psycopg2)
- Apache Airflow 2.9
- PostgreSQL 15
- Docker / Docker Compose

## Как запустить

1. `docker compose up airflow-init`
2. `docker compose up -d`
3. `docker compose exec airflow-scheduler pip install psycopg2-binary requests`
4. Открыть http://localhost:8080 (airflow/airflow)
5. Включить DAG `api_to_postgres_etl` и запустить

## Проверка данных

DBeaver: `localhost:5433`, db `de_test_db`, user `de_user`, password `de_password`.

```sql
SELECT * FROM posts LIMIT 10;
```

<img width="1920" height="1040" alt="dbeaver-img" src="https://github.com/user-attachments/assets/ac8230f0-4171-4584-a79a-228f8dc81ad2" />

<img width="1920" height="1040" alt="airflow-img" src="https://github.com/user-attachments/assets/f012ff6d-77fa-49a0-8695-b590f5e22276" />

