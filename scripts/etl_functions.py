import requests
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://jsonplaceholder.typicode.com/posts"

DB_CONFIG = {
    "host": "postgres-data",
    "port": 5432,
    "dbname": "de_test_db",
    "user": "de_user",
    "password": "de_password",
}


def extract():
    """Забирает данные из API. Возвращает список словарей."""
    logger.info(f"Fetching data from {API_URL}")
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    logger.info(f"Fetched {len(data)} records")
    return data


def transform(raw_data):
    """Убирает дубли по id. Возвращает очищенный список."""
    seen = set()
    cleaned = []
    for item in raw_data:
        if item["id"] not in seen:
            seen.add(item["id"])
            cleaned.append({
                "id": item["id"],
                "user_id": item["userId"],
                "title": item["title"],
                "body": item["body"],
            })
    logger.info(f"After dedup: {len(cleaned)} records")
    return cleaned


def load(records):
    """Создаёт таблицу (если нет) и вставляет данные."""
    if not records:
        logger.warning("No records to load")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            body TEXT
        )
    """)

    ids = [r["id"] for r in records]
    cursor.execute("DELETE FROM posts WHERE id = ANY(%s)", (ids,))

    for rec in records:
        cursor.execute(
            "INSERT INTO posts (id, user_id, title, body) VALUES (%s, %s, %s, %s)",
            (rec["id"], rec["user_id"], rec["title"], rec["body"]),
        )

    conn.commit()
    cursor.close()
    conn.close()
    logger.info(f"Loaded {len(records)} records into posts")