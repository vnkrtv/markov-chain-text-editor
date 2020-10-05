from typing import Generator
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

    def get_posts(self, habs_list: list = None, tags_list: list = None, count=0) -> Generator:
        if not habs_list and not tags_list:
            sql = 'SELECT * FROM posts'
            sql = sql + 'LIMIT %d' % count if count > 0 else sql
            self.cursor.execute(sql)
        elif habs_list:
            self.__get_posts_by_habs(habs_list, count)
        elif tags_list:
            self.__get_posts_by_tags(tags_list, count)
        posts_gen = (post for post in self.cursor.fetchall())
        return posts_gen

    def get_posts_texts(self, habs_list: list = None, tags_list: list = None, count=0) -> Generator:
        posts_texts_gen = (post[2] for post in self.get_posts(habs_list, tags_list, count))
        return posts_texts_gen

    def __get_posts_by_habs(self, habs_list: list, count=0) -> None:
        sql = '''SELECT P.* 
                   FROM posts P JOIN habs H ON P.post_id = H.post_id
                  WHERE H.hab in (%s)''' % ''.join(["'" + str(hab) + "', " for hab in habs_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        self.cursor.execute(sql)

    def __get_posts_by_tags(self, tags_list: list, count=0) -> None:
        sql = '''SELECT P.* 
                   FROM posts P JOIN tags T ON P.post_id = T.post_id
                  WHERE T.tag in (%s)''' % ''.join(["'" + str(tag) + "', " for tag in tags_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        self.cursor.execute(sql)
