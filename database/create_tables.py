import psycopg2

from table_queries import (
    submitted_cases3_table,
    users3_tables,
    admin_user3_query,
)
from postgres import PostgresConnection


def create():
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        table_queries = [
            submitted_cases3_table,
            users3_tables,
            admin_user3_query,
        ]
        for table_query in table_queries:
            try:
                cursor.execute(table_query)
            except psycopg2.IntegrityError as e:
                pass
