import psycopg2

class RedditTables():

    def __init__(self):

        self._db_connection = psycopg2.connect(database = 'postgres',
                                         user = 'postgres', 
                                         password = 'Economics3$',
                                         host = 'aws-crypto-db.c49synhfql06.us-east-2.rds.amazonaws.com', 
                                         port = '5432')
        
        self._db_cur = self._db_connection.cursor()

    # def twitter_lc_table(self):

    #     self._db_cur.execute(' DROP TABLE IF EXISTS twitter_line_chart')

    #     self._db_cur.execute(' CREATE TABLE twitter_line_chart(halfhour TEXT, count INT)')

    #     self._db_cur.execute("""  INSERT INTO twitter_line_chart(halfhour, count)
    #                               SELECT halfhour, count 
    #                               FROM (SELECT COUNT(*), round_minutes((date_created::timestamp without time zone at time zone 'utc' at time zone 'est'), 30) AS HALFHOUR  
    #                               FROM public.twitter_stream 
    #                               GROUP BY 2
    #                               ORDER BY 2 DESC LIMIT 20) AS SQ1 
    #                               ORDER BY halfhour ASC""")

    #     self._db_connection.commit()

    # def twitter_sentiment_table(self):

    #     self._db_cur.execute(' DROP TABLE IF EXISTS twitter_sentiment_table ')

    #     self._db_cur.execute(' CREATE TABLE twitter_sentiment_table(count INT) ')

    #     self._db_cur.execute(""" INSERT INTO twitter_sentiment_table(count)
    #                              SELECT count
    #                              FROM (SELECT COUNT(sentiment) FROM public.twitter_stream
    #                              WHERE sentiment IS NOT NULL
    #                              GROUP BY sentiment) AS SQ1 """)

    #     self._db_connection.commit()

    def reddit_sentiment_table(self):

        self._db_cur.execute(' DROP TABLE IF EXISTS reddit_sentiment_table ')

        self._db_cur.execute(' CREATE TABLE reddit_sentiment_table(count INT) ')

        self._db_cur.execute(""" INSERT INTO reddit_sentiment_table(count)
                                 SELECT count
                                 FROM (SELECT COUNT(sentiment) FROM public.reddit_stream
                                 WHERE sentiment IS NOT NULL
                                 GROUP BY sentiment) AS SQ1 """)

        self._db_connection.commit()

    # def twitter_median_table(self):

    #     self._db_cur.execute(' DROP TABLE IF EXISTS twitter_median_table')

    #     self._db_cur.execute(' CREATE TABLE twitter_median_table(count TEXT) ')

    #     self._db_cur.execute(""" INSERT INTO twitter_median_table(count)
    #                              SELECT count
    #                              FROM (SELECT PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY sentiment) AS count
    #                              FROM public.twitter_stream) AS SQ1 """)

    #     self._db_connection.commit()

    def reddit_median_table(self):

        self._db_cur.execute(' DROP TABLE IF EXISTS reddit_median_table')

        self._db_cur.execute(' CREATE TABLE reddit_median_table(count TEXT) ')

        self._db_cur.execute(""" INSERT INTO reddit_median_table(count)
                                 SELECT count
                                 FROM (SELECT PERCENTILE_DISC(0.5) WITHIN GROUP(ORDER BY sentiment) AS count
                                 FROM public.reddit_stream) AS SQ1 """)

        self._db_connection.commit()

    # def twitter_total_table(self):

    #     self._db_cur.execute(' DROP TABLE IF EXISTS twitter_total_table')

    #     self._db_cur.execute(' CREATE TABLE twitter_total_table(count TEXT) ')

    #     self._db_cur.execute(""" INSERT INTO twitter_total_table(count)
    #                              SELECT SUM(count)
    #                              FROM (SELECT COUNT(*), round_minutes((date_created::timestamp without time zone at time zone 'utc' at time zone 'est'), 30) AS HALFHOUR  
    #                               FROM public.twitter_stream 
    #                               GROUP BY 2
    #                               ORDER BY 2) AS SQ1 """)

    #     self._db_connection.commit()


if __name__ == '__main__':

    rc = RedditTables()

    #tlc.twitter_lc_table() depricated

    rc.reddit_sentiment_table()

    rc.reddit_median_table()

    #tlc.twitter_total_table() depricated

