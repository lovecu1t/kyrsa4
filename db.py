import psycopg2


def get_connection():
    """Повертає підключення до бази даних PostgreSQL"""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="kyrsa4",
        user="postgres",
        password="8787327"
    )
