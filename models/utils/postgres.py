import psycopg2


class PostgresStorage:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    @staticmethod
    def connect(host, port=5432, user='postgres', password='password', dbname='habr'):
        return PostgresStorage(psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=dbname)
        )

    def get_posts(self) -> list:
        self.cursor.execute('SELECT * FROM posts')
        posts = list(self.cursor.fetchall())
        return posts

    def get_posts_texts(self) -> list:
        posts_list = self.get_posts()
        return [post[2] for post in posts_list]
