from typing import Generator
from engine.markov import PostgresStorage


class HabrStorage(PostgresStorage):
    """
    Class for loading posts from habr.com stored in PostgreSQL
    """

    def get_posts(self,
                  count: int = 0,
                  habs_list: list = None,
                  tags_list: list = None) -> Generator:
        if not habs_list and not tags_list:
            cursor = self.conn.cursor()
            sql = 'SELECT * FROM posts'
            if count:
                sql += ' LIMIT %d' % count
            cursor.execute(sql)
            return (post for post in cursor.fetchall())
        elif habs_list:
            return self.__get_posts_by_habs(count, habs_list)
        elif tags_list:
            return self.__get_posts_by_tags(count, tags_list)

    def get_posts_texts(self,
                        count: int = 0,
                        habs_list: list = None,
                        tags_list: list = None) -> Generator:
        posts_texts_gen = (post[2] for post in self.get_posts(count, habs_list, tags_list))
        return posts_texts_gen

    def __get_posts_by_habs(self,
                            count: int,
                            habs_list: list) -> Generator:
        sql = '''SELECT P.* 
                   FROM posts P JOIN habs H ON P.post_id = H.post_id
                  WHERE H.hab in (%s)''' % ''.join(["'" + str(hab) + "', " for hab in habs_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return (post for post in cursor.fetchall())

    def __get_posts_by_tags(self,
                            count: int,
                            tags_list: list) -> Generator:
        sql = '''SELECT P.* 
                   FROM posts P JOIN tags T ON P.post_id = T.post_id
                  WHERE T.tag in (%s)''' % ''.join(["'" + str(tag) + "', " for tag in tags_list])[:-2]
        sql = sql + " LIMIT %d" % count if count > 0 else sql
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return (post for post in cursor.fetchall())
