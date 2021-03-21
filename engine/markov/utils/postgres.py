from typing import Generator, List

import psycopg2


class PostgresStorage:
    """
    Base class for working with PostgreSQL
    """

    conn: psycopg2.extensions.connection

    def __init__(self, conn: psycopg2.extensions.connection):
        self.conn = conn

    @classmethod
    def connect(cls,
                host: str,
                port: int = 5432,
                user: str = 'postgres',
                password: str = 'password',
                dbname: str = 'postgres'):
        return cls(conn=psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=dbname)
        )

    def exec_query(self, query: str, params: List[str]) -> Generator:
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e
        return cursor.fetchall()

    def exec(self, sql: str, params: List[str]):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params)
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e
        self.conn.commit()
