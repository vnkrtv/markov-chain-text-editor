import psycopg2


class PostgresStorage:

    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    @staticmethod
    def connect(host, port=5432, user='postgres', password='password', dbname='habr'):
        return PostgresStorage(conn=psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=dbname)
        )

    def get_posts(self, count=0) -> list:
        if count > 0:
            self.cursor.execute('SELECT * FROM posts LIMIT %d' % count)
        else:
            self.cursor.execute('SELECT * FROM posts')
        posts = list(self.cursor.fetchall())
        return posts

    def get_posts_texts(self, count=0) -> list:
        posts_list = self.get_posts(count)
        return [post[2] for post in posts_list]
